import json
import requests
import pandas as pd
import numpy as np
from datetime import datetime, date
from typing import Union

from databricks import sql

from pyspark import SparkContext
from pyspark.sql import SparkSession, types as t
from pyspark.sql.dataframe import DataFrame


permitted_data_types = ["string", "int", "long", "decimal", "float", "double", "boolean", "timestamp", "date"]


def get_or_create_spark_session() -> (SparkSession, SparkContext, str):
    """
    Added this config: .config('spark.sql.debug.maxToStringFields', 2000), to prevent the following WARNING Message
    WARN package: Truncated the string representation of a plan since it was too large. This behavior can be adjusted by setting 'spark.sql.debug.maxToStringFields'.
    Added this config: .config("spark.driver.memory", "9g"), to prevent the following WARNING Message
    WARN MemoryManager: Total allocation exceeds 95.00% (1,020,054,720 bytes) of heap memory Scaling row group sizes to 95.00% for 8 writers
    Without the config, the executor only has 434.4 MiB storage memory (as shown in the spark UI)
    With the config, the executor has up to 3.4 GiB for 6gb and 5.2 GiB for 9gb (as shown in the spark UI)
    :return: session
    """
    spark = SparkSession.builder \
        .appName("Data Normalization Task") \
        .enableHiveSupport() \
        .config('spark.sql.debug.maxToStringFields', 2000) \
        .config("spark.driver.memory", "9g") \
        .getOrCreate()

    return spark


def get_sql_endpoint_id(token, hostname) -> str:
    HEADERS = {
        "Authorization": f"Bearer {token}"
    }
    res = requests.get(url=f"https://{hostname}/api/2.0/preview/sql/data_sources", headers=HEADERS)
    sql_data_sources = json.loads(res.content.decode())
    sql_endpoint_id = [
        data_source["endpoint_id"] for data_source in sql_data_sources if data_source["name"] == "SQLEndpoint"
    ][0]
    return sql_endpoint_id


def retrieve_sql_connection(token, hostname, sql_endpoint_id):
    connection = sql.connect(
        server_hostname=hostname,
        http_path=f"/sql/1.0/warehouses/{sql_endpoint_id}",
        access_token=token
    )
    print("databricks sql connection established")
    return connection


def sql_engine(sql_connection, query, catalog: str) -> pd.DataFrame:
    cursor = sql_connection.cursor()

    try:
        if catalog:
            cursor.execute(f"use catalog {catalog};")
        cursor.execute(query)
        names = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        return pd.DataFrame(rows, columns=names)

    finally:
        if cursor is not None:
            cursor.close()


def collect_insert_statement_values_str(df_dict_list: list, table_col_names: list) -> list:
    insert_values_str = []
    for row in df_dict_list:
        value_str_list = []
        for i in range(len(table_col_names)):
            if isinstance(row[table_col_names[i]], str):
                if row[table_col_names[i]] in ["nan", "NaT"]:
                    value_str_list.append("null")
                else:
                    cell_data = row[table_col_names[i]].replace("'", "\\'")
                    value_str_list.append(f"'{cell_data}'")
            elif isinstance(row[table_col_names[i]], datetime):
                pass
            elif isinstance(row[table_col_names[i]], date):
                pass
            else:
                value_str_list.append(str(row[table_col_names[i]]))

        insert_values_str.append("("+", ".join(value_str_list)+")")

    return insert_values_str


def get_spark_data_type(data_type: str):
    spark_type = t.StringType()
    if data_type == "int":
        spark_type = t.IntegerType()
    elif data_type == "long":
        spark_type = t.LongType()
    elif data_type == "double":
        spark_type = t.DoubleType()
    elif data_type == "float":
        spark_type = t.FloatType()
    elif data_type == "decimal":
        spark_type = t.DecimalType()
    elif data_type == "boolean":
        spark_type = t.BooleanType()
    elif data_type == "timestamp":
        spark_type = t.TimestampType()
    elif data_type == "date":
        spark_type = t.DateType()

    return spark_type


def build_spark_schema(df: pd.DataFrame) -> t.StructType:
    df_dict_list = df.astype(str).to_dict(orient="records")
    struct_field_list = []
    for row in df_dict_list:
        struct_field_list.append(t.StructField(row["col_name"], get_spark_data_type(row["data_type"])))

    return t.StructType(struct_field_list)


def check_for_permitted_datatypes(table_schema_dict_list: list):
    table_data_types = list(set([el["data_type"] for el in table_schema_dict_list]))
    un_permitted_data_types = []
    for table_dtype in table_data_types:
        if table_dtype not in permitted_data_types:
            un_permitted_data_types.append(table_dtype)

    if un_permitted_data_types:
        raise ValueError(f"""
            The target table contains the following data types that are currently not supported in the write feature:\n
            {un_permitted_data_types}
        """)


def check_for_columns_match(table_col_names: list, df_columns: list, target_table):
    df_col_names = [_col.lower() for _col in df_columns]
    table_col_names = [_col.lower() for _col in table_col_names]
    df_col_names.sort()
    table_col_names.sort()
    if df_col_names != table_col_names:
        raise ValueError(f"""
            pandas DataFrame columns does not match target table columns in {target_table}\n
            df  cols: {df_col_names}\n
            tbl cols: {table_col_names}
        """)


def check_for_data_type_casting(table_describe_df: pd.DataFrame, df: Union[pd.DataFrame, DataFrame], to_spark_fcn):
    df_spark_schema = build_spark_schema(table_describe_df)
    if isinstance(df, DataFrame):
        df = df.toPandas()
    spark_df = to_spark_fcn(df, df_spark_schema)
    casted_pd_df = spark_df.toPandas()
    df = df[spark_df.columns]

    src_dict_list = df.astype(str).to_dict(orient="records")
    casted_dict_list = casted_pd_df.astype(str).to_dict(orient="records")
    if src_dict_list != casted_dict_list:
        if len(src_dict_list) != len(casted_dict_list):
            missing_rows = [json.dumps(el) for el in src_dict_list if el not in casted_dict_list]
            missing_rows_str = "\n".join(missing_rows[:10 if len(missing_rows) >= 10 else len(missing_rows)]) + (f"\n... and {len(missing_rows)-10} more" if len(missing_rows) > 10 else "")
            raise ValueError(f"""
                Number of rows dont match after casting source df to expected spark table schema data types
                source_pd_df rows: {len(src_dict_list)}
                casted_pd_df rows: {len(casted_dict_list)}
                missing rows after casting to expected table schema column data types:\n{missing_rows_str}
            """)
        else:
            row_diffs = []
            for i in range(len(src_dict_list)):
                if src_dict_list[i] != casted_dict_list[i]:
                    row_diffs.append(f"""
                        row: {i}
                        source_data: {src_dict_list[i]}
                        casted_data: {casted_dict_list[i]}
                    """)
            row_diffs_str = '\n'.join(row_diffs)
            raise ValueError(f"Rows with differences between the source data and casted data were found:\n{row_diffs_str}")


class Bridge:
    def __init__(self, hostname: str, token: str, spark: SparkSession = None, catalog: str = None):
        if not spark:
            spark = get_or_create_spark_session()
        self.spark = spark
        sql_endpoint_id = get_sql_endpoint_id(token, hostname)
        self.sql_connection = retrieve_sql_connection(token, hostname, sql_endpoint_id)
        self.catalog = catalog

    def write_df_to_table(self, df: Union[pd.DataFrame, DataFrame], target_table):
        table_describe_df = sql_engine(self.sql_connection, f"DESCRIBE TABLE {target_table}", catalog=self.catalog)
        table_schema_dict_list = table_describe_df.astype(str).to_dict(orient="records")
        table_col_names = [el["col_name"] for el in table_schema_dict_list]

        df = df.toPandas() if isinstance(df, DataFrame) else df
        df_dict_list = df.replace({None: np.nan}).astype(str).to_dict(orient="records")

        check_for_permitted_datatypes(table_schema_dict_list)
        check_for_columns_match(table_col_names, df.columns.tolist(), target_table)
        check_for_data_type_casting(table_describe_df, df, self.to_spark_df)

        insert_values_str = collect_insert_statement_values_str(df_dict_list, table_col_names)
        insert_query = f"""
        INSERT INTO {target_table} ({', '.join(table_col_names)})
        VALUES {', '.join(insert_values_str)};
        """
        ret_df, _ = self.execute_query(insert_query)

        return ret_df

    def to_spark_df(self, pandas_df: pd.DataFrame, spark_schema: t.StructType = None):
        rdd = self.spark.sparkContext.parallelize([pandas_df.astype(str).to_json(orient="records")])
        df = self.spark.read.json(rdd)
        if spark_schema:
            for field_schema in spark_schema:
                df = df.withColumn(field_schema.name, df[field_schema.name].cast(field_schema.dataType))

        return df

    def execute_query(self, sql_query: str) -> (pd.DataFrame, t.StructType):
        start_time = datetime.now()
        try:
            df = sql_engine(self.sql_connection, sql_query, catalog=self.catalog)
            df_spark_schema = None
            try:
                if not df.empty and df.columns.tolist() != ["num_affected_rows", "num_inserted_rows"]:
                    query_describe_df = sql_engine(self.sql_connection, f"DESCRIBE QUERY {sql_query}", catalog=self.catalog)
                    df_spark_schema = build_spark_schema(query_describe_df)
            except Exception as e:
                print(e)
            duration = (datetime.now() - start_time).total_seconds()
        except Exception as e:
            print(e)
            print(f"This query was failed during execution:\n{sql_query}")
            raise ValueError(e)

        return df, df_spark_schema

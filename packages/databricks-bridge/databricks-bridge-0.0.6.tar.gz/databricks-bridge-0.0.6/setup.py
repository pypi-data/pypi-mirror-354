from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.6'
DESCRIPTION = 'Databricks read and write with sql connection'
LONG_DESCRIPTION = '''
Databricks read and write data from and to databricks tables via insert statement direct write, pandas or spark dataframes to insert statement conversion write

## Requirements
Python 3.7 or above is required.

## Prerequisite:
- Java
- Python
- Pyspark
- Pandas
- Numpy

Although the installation of this package installs pyspark, pandas, and numpy, the spark environment isnt set up automatically.
The machine should be able to create a spark session and create spark and pandas dataframes.

To confirm if pyspark is running as expected, run the following python script:
```
from pyspark.sql import SparkSession
import pandas as pd

spark = SparkSession.builder.appName("Databricks Bridge Test").enableHiveSupport().getOrCreate()
dict_data = [
    {"name": "Tom", "age": 20, "dob": "2000-10-31"},
    {"name": "Dick", "age": 21, "dob": "1999-10-30"},
    {"name": "Harry", "age": 22, "dob": "1998-10-29"}
]
spark_df = spark.createDataFrame(dict_data)
spark_df.show()

pd_df = pd.DataFrame(dict_data)
print(pd_df)
```

Should return:
```
+---+----------+-----+
|age|       dob| name|
+---+----------+-----+
| 20|2000-10-31|  Tom|
| 21|1999-10-30| Dick|
| 22|1998-10-29|Harry|
+---+----------+-----+
```

```
    name  age         dob
0    Tom   20  2000-10-31
1   Dick   21  1999-10-30
2  Harry   22  1998-10-29
```
If this runs without errors and the dataframe prints are returned on the console, then pyspark and pandas are set up properly.

If not, then please install openjdk

## Usage
- Initialization
  - ```
    from databricks_bridge import Bridge
    bridge = Bridge(hostname="<host_id>.cloud.databricks.com", token="<token>", catalog="<target_catalog>")
    # catalog is an optional argument. If not specified, the default catalog in your databricks workspace will be used
    ```
- Run queries without data returns
  - ```
    bridge.execute_query("create database if not exists bridge_test_db;")
    bridge.execute_query("""
        create table if not exists bridge_test_db.students (
            name string,
            age int,
            dob date,
            last_active timestamp,
            reg_date date
        );""")
    ```
- Write into tables with sql insert statement
  - ```
    bridge.execute_query("""
        insert into bridge_test_db.students (age, name, dob, last_active, reg_date)
        values
            (18, 'Rachel', '1999-11-01', '2023-11-01 20:36:31.365375', '2023-11-01'),
            (19, 'Harriet', '1999-11-02', '2023-11-01 20:36:31.365375', '2022-11-01');
    """)
    ```
- Write pandas or spark dataframes into databricks tables
  - ```
    new_data = [
        {"name": "Tom", "age": 20, "dob": "1999-10-31", "last_active": datetime.now(), "reg_date": datetime.today().date()},
        {"name": "Dick", "age": 21, "dob": "1999-10-30", "last_active": datetime.now(), "reg_date": datetime.today().date()},
        {"name": "Harry", "age": 22, "dob": "1999-10-29", "last_active": datetime.now(), "reg_date": datetime.today().date()}
    ]
    new_pd_df = pd.DataFrame(new_data)
    bridge.write_df_to_table(df=new_pd_df, target_table="bridge_test_db.students")

    new_spark_df = bridge.spark.createDataFrame(new_data)
    bridge.write_df_to_table(df=new_spark_df, target_table="bridge_test_db.students")
    ```
- Run queries with dataframes returns
  - ```
    pd_df, spark_schema = bridge.execute_query("select * from bridge_test_db.students")
    ```
- Convert returned default pandas dataframe to spark dataframe with exact schema match
  - ```
    spark_df = bridge.to_spark_df(pd_df, spark_schema)
    ```
- Convert returned default pandas dataframe to spark dataframe without exact schema match
  - ```
    spark_df = bridge.to_spark_df(pd_df)
    ```
'''

# Setting up
setup(
    name="databricks-bridge",
    version=VERSION,
    author="Y-Tree (Saeed Falowo)",
    author_email="saeed@y-tree.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['pandas', 'numpy', 'databricks-sql-connector', 'pyspark'],
    keywords=['python', 'databricks', 'pyspark', 'sql', 'dataframe'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)

'''
python3 setup.py sdist bdist_wheel
twine upload dist/* 
username = __token__
password = <api_token>

https://pypi.org/project/databricks-bridge/
'''

-- Step 1: Set up your warehouse, database, and schema
CREATE WAREHOUSE IF NOT EXISTS my_warehouse
WITH WAREHOUSE_SIZE = 'X-SMALL'
AUTO_SUSPEND = 300
AUTO_RESUME = TRUE;

CREATE DATABASE IF NOT EXISTS my_database;

USE DATABASE my_database;
CREATE SCHEMA IF NOT EXISTS my_schema;

USE WAREHOUSE my_warehouse;
USE DATABASE my_database;
USE SCHEMA my_schema;

-- Step 2: Create a file format for JSON
CREATE FILE FORMAT my_json_format
    TYPE = 'JSON'
    STRIP_OUTER_ARRAY = TRUE;

-- Step 3: Create an internal stage (assuming your file is local)
CREATE STAGE my_stage
    FILE_FORMAT = my_json_format;

-- If your file is in S3, the stage creation would look like this:
-- CREATE STAGE my_S3_stage
--     URL = 's3://mybucket/my/path/'
--     FILE_FORMAT = my_json_format
--     CREDENTIALS = (AWS_KEY_ID = 'my_aws_key_id' AWS_SECRET_KEY = 'my_aws_secret_key');

-- Step 5: Create a table for storing JSON data
CREATE TABLE my_table (
    id INT AUTOINCREMENT PRIMARY KEY,
    data VARIANT
);

-- Step 4 & 6: Upload your JSON file to the stage and copy data into the table
-- For an internal stage:
PUT file://app/data/semi_structured_data.json @my_stage;
COPY INTO my_table(data)
    FROM @my_stage/semi_structured_data.json
    FILE_FORMAT = (FORMAT_NAME = my_json_format);

-- For an external stage, you would skip the PUT command and directly use COPY INTO with the external stage's path

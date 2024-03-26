import os

import pandas as pd
import snowflake.connector

# Snowflake connection parameters
conn_params = {
    "user": os.getenv('SNOWFLAKE_USER'),
    "password": os.getenv('SNOWFLAKE_PASSWORD'),
    "account": os.getenv('SNOWFLAKE_ACCOUNT'),
    "warehouse": "MY_WAREHOUSE",
    "database": "MY_DATABASE",
    "schema": "MY_SCHEMA"
}


def query_snowflake(sql_query):
    """
    Queries Snowflake and returns the result as a pandas DataFrame.

    Parameters:
    - sql_query (str): The SQL query to execute.

    Returns:
    - DataFrame: The query results as a pandas DataFrame.
    """

    # Establish connection
    ctx = snowflake.connector.connect(
        user=conn_params["user"],
        password=conn_params["password"],
        account=conn_params["account"],
        warehouse=conn_params["warehouse"],
        database=conn_params["database"],
        schema=conn_params["schema"],
    )

    # Create a cursor object
    cur = ctx.cursor()

    try:
        # Execute the query
        cur.execute(sql_query)
        # Fetch the results
        rows = cur.fetchall()
        # Fetch column names
        columns = [col[0] for col in cur.description]
        # Create DataFrame from fetched data
        df = pd.DataFrame(rows, columns=columns)

    finally:
        # Close the cursor and connection
        cur.close()
        ctx.close()

    return df


if __name__ == "__main__":
    query = """
    SELECT
        DATA:UserID::INT AS USER_ID,
        DATA:UserActivity:"Design Idea"::STRING AS DESIGN_IDEA,
        DATA:UserActivity:"Engagement Level"::STRING AS ENGAGEMENT_LEVEL
    FROM
        MY_TABLE LIMIT;
    """

    # Query Snowflake and get the result as a DataFrame
    df = query_snowflake(query)

    # Display the DataFrame
    print(df.head())

    # Print number of unique users and Design Ideas
    print(f"Number of unique users: {df['USER_ID'].nunique()}")
    print(f"Number of unique Design Ideas: {df['DESIGN_IDEA'].nunique()}")

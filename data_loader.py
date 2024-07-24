from snowflake.connector import connect
import pandas as pd
import config
import streamlit as st

# Cache the query data for efficiency
@st.cache_data 
# Setup and fetch data from Snowflake data warehouse
def fetch_data(table_type):

    sf_conn = connect(
        user=config.SNOWFLAKE_USER,
        password=config.SNOWFLAKE_PASSWORD,
        account=config.SNOWFLAKE_ACCOUNT,
        warehouse=config.SNOWFLAKE_WAREHOUSE,
        database=config.SNOWFLAKE_DATABASE,
        schema=config.SNOWFLAKE_SCHEMA,
        role=config.SNOWFLAKE_ROLE  
    )
    def get_table(sf_conn, snowflake_table):
        try:
            with sf_conn.cursor() as sf_cursor:
                sf_cursor.execute(f"SELECT * FROM {snowflake_table}")
                # Fetch all rows as a list of tuples
                rows = sf_cursor.fetchall()
                
                # Get column names from the cursor description
                columns = [desc[0] for desc in sf_cursor.description]
                
                # Convert the list of tuples into a pandas DataFrame
                df = pd.DataFrame(rows, columns=columns)
                
            return df
        except Exception as e:
            print(f"Error fetching data from Snowflake: {e}")
            return pd.DataFrame()  # Return an empty DataFrame in case of error

    # Fetch tables based on function parameters
    if table_type == 'listing':
        main_table = get_table(sf_conn, "TEST_DB.PUBLIC.LISTING_VIEW")
        main_table = main_table.dropna()
    elif table_type == 'host':
        main_table = get_table(sf_conn, "TEST_DB.PUBLIC.HOST_VIEW")
    else:
        print("Invalid load parameter!")
        main_table = pd.DataFrame()  # Return an empty DataFrame for invalid table type
    
    sf_conn.close()
    return main_table
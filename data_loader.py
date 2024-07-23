from snowflake.snowpark import Session
from snowflake.snowpark.exceptions import SnowparkSQLException
import pandas as pd
import config
import streamlit as st

@st.cache_data
def load_data(table_type):
    try:
        # Set up your Snowflake connection parameters
        connection_param = {
            "account": config.SNOWFLAKE_ACCOUNT,
            "user": config.SNOWFLAKE_USER,
            "password": config.SNOWFLAKE_PASSWORD,
            "role": config.SNOWFLAKE_ROLE,
            "database": config.SNOWFLAKE_DATABASE,
            "schema": config.SNOWFLAKE_SCHEMA
        }
        # creating a session object
        session = Session.builder.configs(connection_param).create()

        # print values from session object to test
        print("\n\t Connection successful!")

        if table_type == 'listing':
            main_table = session.table("TEST_DB.PUBLIC.LISTING_VIEW").to_pandas()
            main_table = main_table.dropna()
        elif table_type == 'host':
            main_table = session.table("TEST_DB.PUBLIC.HOST_VIEW").to_pandas()
        else:
            print("Invalid load parameter!")
        
    # Error handling blocks
    except SnowparkSQLException as e:
        print(f"Snowpark SQL Exception: {e}")
        main_table = pd.DataFrame()  # Return an empty DataFrame if there's an SQL error
    except Exception as e:
        print(f"An error occurred: {e}")
        main_table = pd.DataFrame()  # Return an empty DataFrame if there's a general error
    finally:
        try:
            session.close()
        except Exception as e:
            print(f"Failed to close session: {e}")

    return main_table


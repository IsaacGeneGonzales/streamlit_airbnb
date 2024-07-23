import streamlit as st

def display_home():
    container = st.container(border = True)
    container.header("Application Summary")
    container.write(
        'The application leverages the Snowpark framework to extract data from a Snowflake database. This database integrates compiled tables derived from two Airbnb listing CSV files, specifically focusing on property listings in Texas and Boston. For the frontend interface, the application employs the Streamlit framework to present the data visually and interactively.')

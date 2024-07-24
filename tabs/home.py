import streamlit as st

def display_home():
    container = st.container(border = True)
    container.write(
        'This application serves as a Streamlit-Snowflake integration exercise that lets the user explore various property listings KPIs and interact with dynamic figures.')
import streamlit as st
from data_loader import fetch_data
import pandas as pd

def display_listings():
    st.header('PROPERTY LISTINGS')
    st.markdown('_This table consist of airbnb listings posted on a specified date. Unique listings are identified by the id field._')
    with st.expander("Data Preview"):
        st.dataframe(fetch_data("listing"))

    st.header('HOST INFORMATION')
    st.markdown('_This table consist of airbnb host information found on the listings table. Unique hosts are identified by host id field._')
    with st.expander("Data Preview"):
        st.dataframe(fetch_data("host"))
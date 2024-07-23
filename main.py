import streamlit as st
from tabs.home import display_home
from tabs.data_page import display_listings
from tabs.dashboard import display_dashboard

st. set_page_config(layout="wide")
st.title('PROPERTY LOGDING APP')
tab_names = ["Home", "Listing and Host Tables", "Dashboard"]
tabs = st.tabs(tab_names)

# Call the respective function based on the selected tab
with tabs[0]:
    display_home()

with tabs[1]:
    display_listings()

with tabs[2]:
    display_dashboard()

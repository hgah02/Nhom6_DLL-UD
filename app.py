from pages.home import HomePage
import streamlit as st

st.set_page_config(layout="wide")

page = HomePage()
page.init()

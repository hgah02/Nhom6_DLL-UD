import streamlit as st
from bases.page import Page

class Home(Page):
    def view(self):
        st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

        st.title("Trang chủ")

        if st.button("Đăng ký"):
            st.switch_page("pages/register.py")
        if st.button("Đăng nhập"):
            st.switch_page("pages/login.py")
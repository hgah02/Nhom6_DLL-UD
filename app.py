import streamlit as st
from pages.home import HomePage
from pages.upload import UploadPage
from pages.me import MyPage
from bases.page import Page

st.set_page_config(layout="wide")

def get_page(header_menu):
    if header_menu == "Trang chủ":
        return HomePage()
    elif header_menu == "Đăng ảnh":
        return UploadPage()
    elif header_menu == "Ảnh của tôi":
        return MyPage()
    return HomePage()

if not st.session_state.get("header_menu"):
    st.session_state["header_menu"] = "Trang chủ"

page = get_page(st.session_state.header_menu)
page.init()

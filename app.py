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
        if not Page.get_auth_id():
            st.session_state["header_menu"] = "Trang chủ"
            st.toast("Vui lòng đăng nhập để tiếp tục.")
            return HomePage()
        return UploadPage()
    elif header_menu == "Ảnh của tôi":
        if not Page.get_auth_id():
            st.session_state["header_menu"] = "Trang chủ"
            st.toast("Vui lòng đăng nhập để tiếp tục.")
            return HomePage()
        return MyPage()
    return HomePage()

if not st.session_state.get("header_menu"):
    st.session_state["header_menu"] = "Trang chủ"

page = get_page(st.session_state.header_menu)
page.init()

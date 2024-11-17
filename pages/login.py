import streamlit as st
from bases.page import Page

class LoginPage(Page):
    def login(self, username, password):
        if (username == "") or (password == ""):
            st.error("Vui lòng điền đầy đủ thông tin.")
            return
        # TODO: Check if username exists in the database
        # TODO: Check if password is correct
        # TODO: Set the session state to logged in

    def view(self):
        st.set_page_config(layout="centered", initial_sidebar_state="collapsed")
        st.title("Đăng nhập")
        username = st.text_input("Tên người dùng")
        password = st.text_input("Mật khẩu", type="password")

        left, right = st.columns(2, vertical_alignment="center")
        if left.button("Đăng nhập"):
            self.login(username, password)
        right.page_link("pages/register.py", label="Chưa có tải khoản?")

page = LoginPage()
page.init()

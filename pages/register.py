import streamlit as st
from bases.page import Page

class Register(Page):
    def register(self, username, password, password_confirmation):
        if (username == "") or (password == "") or (password_confirmation == ""):
            st.error("Vui lòng điền đầy đủ thông tin.")
            return False
        if password != password_confirmation:
            st.error("Mật khẩu không khớp.")
            return False
        # TODO: Check if username already exists in the database
        # TODO: Add the new user to the database

    def view(self):
        st.set_page_config(layout="centered", initial_sidebar_state="collapsed")
        st.title("Tạo tài khoản mới")
        username = st.text_input("Tên người dùng")
        password = st.text_input("Mật khẩu", type="password")
        password_confirmation = st.text_input("Nhập lại mật khẩu", type="password")

        left, right = st.columns(2, vertical_alignment="center")
        if left.button("Đăng ký"):
            self.register(username, password, password_confirmation)
        right.page_link("pages/login.py", label="Đã có tải khoản?")

page = Register()
page.init()

import streamlit as st
from bases.page import Page
from repositories.user import user_repository
from bcrypt import hashpw, gensalt

class RegisterPage(Page):
    def register(self, username, password, password_confirmation):
        if (username == "") or (password == "") or (password_confirmation == ""):
            st.error("Vui lòng điền đầy đủ thông tin.")
            return
        if password != password_confirmation:
            st.error("Mật khẩu không khớp.")
            return

        existing_user = user_repository.find_by_username(username)
        if existing_user:
            st.error("Tên người dùng đã tồn tại.")
            return

        hashed_password = hashpw(password.encode(), salt=gensalt())
        user_repository.create_user(username, hashed_password)

        st.success("Đăng ký thành công.")

    def view(self):
        st.title("Tạo tài khoản mới")
        username = st.text_input("Tên người dùng")
        password = st.text_input("Mật khẩu", type="password")
        password_confirmation = st.text_input("Nhập lại mật khẩu", type="password")

        left, right = st.columns([0.1, 1.5], vertical_alignment="center")
        if left.button("Đăng ký"):
            self.register(username, password, password_confirmation)
        right.page_link("pages/login.py", label="Đã có tải khoản?")

page = RegisterPage()
page.init()

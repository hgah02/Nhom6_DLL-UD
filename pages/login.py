import streamlit as st
from bases.page import Page
from repositories.user import user_repository
from bcrypt import checkpw

class LoginPage(Page):
    def login(self, username, password):
        if (username == "") or (password == ""):
            st.error("Vui lòng điền đầy đủ thông tin.")
            return

        user = user_repository.find_by_username(username)
        if not user or checkpw(password.encode(), user["password"]):
            st.error("Sai tên người dùng hoặc mật khẩu.")
            return

        self.set_authentication_info(username)

        st.switch_page("app.py")

    def view(self):
        st.title("Đăng nhập")
        username = st.text_input("Tên người dùng")
        password = st.text_input("Mật khẩu", type="password")

        left, right = st.columns(2, vertical_alignment="center")
        if left.button("Đăng nhập"):
            self.login(username, password)
        right.page_link("pages/register.py", label="Chưa có tải khoản?")

page = LoginPage()
page.init()

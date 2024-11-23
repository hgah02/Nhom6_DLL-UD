import streamlit as st
from bases.page import Page
from repositories.user import user_repository
from bcrypt import checkpw

class LoginPage(Page):
    def __init__(self):
        super().__init__(is_hide_header=True)

    def login(self, username, password):
        if (username == "") or (password == ""):
            st.error("Vui lòng điền đầy đủ thông tin.")
            return

        user = user_repository.find_by_username(username)
        print("userLoggedIn", user)
        if not user or not checkpw(password.encode(), user["password"]):
            st.error("Sai tên người dùng hoặc mật khẩu.")
            return

        Page.set_authentication_info(str(user["_id"]), username)

        st.switch_page("app.py")
        st.rerun()

    def view(self):
        [_, content, _] = st.columns([1, 6, 1])

        with content:
            st.title("Đăng nhập")
            username = st.text_input("Tên người dùng")
            password = st.text_input("Mật khẩu", type="password")

            left, right = st.columns([3, 7], vertical_alignment="center")
            if left.button("Đăng nhập", key="login"):
                self.login(username, password)
            right.page_link("pages/register.py", label="Chưa có tải khoản?")

page = LoginPage()
page.init()

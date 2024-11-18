import streamlit as st
from bases.page import Page

class HomePage(Page):
    def view(self):
        if (self.is_authenticated()):
            st.title(f"Chào mừng {self.get_auth_username()}!")
            st.write("Bạn đã đăng nhập thành công.")
            if st.button("Đăng xuất"):
                self.remove_authentication_info()
                st.rerun()
        else:
            st.title("Trang chủ")
            if st.button("Đăng ký"):
                st.switch_page("pages/register.py")
            if st.button("Đăng nhập"):
                st.switch_page("pages/login.py")

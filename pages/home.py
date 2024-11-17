import streamlit as st
from bases.page import Page

class HomePage(Page):
    def view(self):
        if 'logged_in' not in st.session_state:
            st.session_state['logged_in'] = False

        if (st.session_state["logged_in"]):
            st.title(f"Chào mừng {st.session_state['username']}!")
            st.write("Bạn đã đăng nhập thành công.")
            st.button("Đăng xuất", on_click=lambda: st.session_state.clear())
        else:
            st.session_state["logged_in"] = False

            st.title("Trang chủ")
            if st.button("Đăng ký"):
                st.switch_page("pages/register.py")
            if st.button("Đăng nhập"):
                st.switch_page("pages/login.py")

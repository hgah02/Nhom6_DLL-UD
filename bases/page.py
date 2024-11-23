from abc import abstractmethod, ABC
import streamlit as st
from streamlit_cookies_manager import EncryptedCookieManager
from streamlit_option_menu import option_menu

class Page(ABC):
    def __init__(self, is_hide_header=False):
        self.is_hide_header = is_hide_header
        Page.cookie = EncryptedCookieManager(prefix="myapp", password="your_secure_password")
        if not Page.cookie.ready():
            st.stop()

    @abstractmethod
    def view(self):
        pass

    @staticmethod
    def set_authentication_info(user_id, username):
        Page.cookie["logged_username"] = username
        Page.cookie["logged_id"] = user_id
        Page.cookie.save()

    @staticmethod
    def remove_authentication_info():
        Page.cookie["logged_username"] = ''
        Page.cookie["logged_id"] = ''
        Page.cookie.save()

    @staticmethod
    def get_auth_username():
        return Page.cookie.get('logged_username')

    @staticmethod
    def get_auth_id():
        return Page.cookie.get('logged_id')

    def header(self):
        if self.is_hide_header:
            return

        [header_left, header_right] = st.columns([12,1], vertical_alignment="center")
        with (header_left):
            menu = option_menu(None, ["Trang chủ", "Đăng ảnh", "Ảnh của tôi"],
                menu_icon="cast",key='header_menu', default_index=0, orientation="horizontal")

        with (header_right):
            if self.get_auth_id():
                if st.button("Đăng xuất"):
                    self.remove_authentication_info()
                    st.rerun()
            else:
                if st.button("Đăng nhập"):
                    st.switch_page("pages/login.py")

    def init(self):
        self.header()
        self.view()

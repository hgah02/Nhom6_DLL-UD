from abc import abstractmethod, ABC
import streamlit as st
from streamlit_cookies_manager import EncryptedCookieManager

class Page(ABC):
    def __init__(self):
        self.cookie = EncryptedCookieManager(prefix="myapp", password="your_secure_password")
        if not self.cookie.ready():
            st.stop()

    @abstractmethod
    def view(self):
        pass

    def set_authentication_info(self, user_id, username):
        self.cookie["logged_username"] = username
        self.cookie["logged_id"] = user_id
        self.cookie.save()

    def remove_authentication_info(self):
        self.cookie["logged_username"] = ''
        self.cookie["logged_id"] = ''
        self.cookie.save()

    def get_auth_username(self):
        return self.cookie.get('logged_username')

    def get_auth_id(self):
        return self.cookie.get('logged_id')

    def init(self):
        self.view()

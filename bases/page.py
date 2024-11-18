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

    def set_authentication_info(self, username):
        self.cookie["auth_info"] = username
        self.cookie.save()

    def remove_authentication_info(self):
        self.cookie["auth_info"] = ''
        self.cookie.save()

    def get_auth(self):
        return self.cookie.get('auth_info')

    def init(self):
        self.view()

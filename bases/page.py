from abc import abstractmethod, ABC
import streamlit as st
from streamlit_cookies_controller import CookieController

class Page(ABC):
    def __init__(self):
        self.cookie = CookieController()

    @abstractmethod
    def view(self):
        pass

    def set_authentication_info(self, username):
        self.cookie.set("is_authenticated", True)
        self.cookie.set("auth_info", username)

    def remove_authentication_info(self):
        self.cookie.remove("is_authenticated")
        self.cookie.remove("auth_info")

    def is_authenticated(self):
        return self.cookie.get("is_authenticated")

    def get_auth_username(self):
        return self.cookie.get('auth_info')

    def init(self):
        self.view()

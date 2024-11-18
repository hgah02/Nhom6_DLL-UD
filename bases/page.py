from abc import abstractmethod, ABC
import streamlit as st
from streamlit_cookies_controller import CookieController

class Page(ABC):
    def __init__(self):
        self.cookie = CookieController()

    @abstractmethod
    def view(self):
        pass

    def init(self):
        self.view()

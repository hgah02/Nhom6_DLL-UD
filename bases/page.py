from abc import abstractmethod, ABC
import streamlit as st

class Page(ABC):
    @abstractmethod
    def view(self):
        pass

    def init(self):
        self.view()

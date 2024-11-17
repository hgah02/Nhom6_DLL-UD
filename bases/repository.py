from abc import ABC
from database.mongo_client import client
import streamlit as st

class Repository(ABC):
    def __init__(self, collection_name: str):
        self.client = client
        self.db = self.client[st.secrets["mongo_db"]["database_name"]]
        self.collection = self.db[collection_name]
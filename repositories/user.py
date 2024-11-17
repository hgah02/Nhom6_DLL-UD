from bases.repository import Repository

class UserRepository(Repository):
    def __init__(self):
        super().__init__(collection_name="users")

    def find_by_username(self, username: str):
        return self.collection.find_one({"username": username})

    def create_user(self, username: str, password: str):
        self.collection.insert_one({"username": username, "password": password})

user_repository = UserRepository()

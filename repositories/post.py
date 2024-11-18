from bases.repository import Repository

class PostRepository(Repository):
    def __init__(self):
        super().__init__(collection_name="posts")

    def create_post(self,title, content, keywords, is_public, image_path, user_id):
        return self.collection.insert_one({
            "title": title,
            "content": content,
            "keywords": keywords,
            "is_public": is_public,
            "image_path": image_path,
            "user_id": user_id
        })

    def find_all(self):
        return self.collection.find()

post_repository = PostRepository()

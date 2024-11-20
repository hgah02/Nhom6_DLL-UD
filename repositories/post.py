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
            "user_id": user_id,
            "likes": []
        })

    def like_post(self, post_id, user_id):
        post = self.collection.find_one({"_id": post_id})
        if user_id in post["likes"]:
            self.collection.update_one(
                {"_id": post_id},
                {"$pull": {"likes": user_id}}
            )
            return False
        self.collection.update_one(
            {"_id": post_id},
            {"$addToSet": {"likes": user_id}}
        )
        return True

    def find_all(self, search=None):
        match_stage = [{"$match": {"is_public": True}}]

        if search:
            match_stage.append({
            "$match": {
                "$or": [
                    {"title": {"$regex": search, "$options": "i"}},
                    {"content": {"$regex": search, "$options": "i"}},
                    {"keywords": {"$in": [search]}}
                ]}
            })

        return list(self.collection.aggregate([
            *match_stage,
            {
                "$lookup": {
                    "from": "users",
                    "localField": "user_id",
                    "foreignField": "_id",
                    "as": "user"
                }
            },
            {
                "$unwind": {
                    "path": "$user",
                    "preserveNullAndEmptyArrays": True
                }
            }
        ]))

post_repository = PostRepository()

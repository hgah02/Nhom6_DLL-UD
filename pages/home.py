import streamlit as st
from bases.page import Page
from repositories.post import post_repository
import os

class HomePage(Page):
    def view(self):
        self.view_header()

        st.session_state.posts = post_repository.find_all()

        search = st.text_input("Tìm kiếm:")
        if (st.button("Tìm kiếm")):
            st.session_state.posts = post_repository.find_all(search)

        max_columns = 4
        grid_columns = st.columns(max_columns)

        posts = st.session_state.posts
        for index, post in enumerate(posts):
            with grid_columns[index % max_columns]:
                # Image
                st.image(os.path.abspath(post['image_path']), use_container_width=True)

                # Content
                st.write(f"**{post['title']}**")
                st.write(post["content"])
                st.write(f"*Đăng bởi: {post['user']['username']}*")

                [download_button, like_button] = st.columns([0.1, 0.9])
                with like_button:
                   if self.get_auth_id():
                        is_liked = self.get_auth_id() in post["likes"]
                        button_label = "👎 Bỏ thích" if is_liked else "👍"
                        if st.button(button_label, key=f"like_{post['_id']}"):
                            if "liked_posts" not in st.session_state:
                                st.session_state.liked_posts = {}
                            liked = post_repository.like_post(post["_id"], self.get_auth_id())
                            st.session_state.liked_posts[post["_id"]] = liked
                            st.rerun()

                # Button handler
                with download_button:
                    with open(os.path.abspath(post['image_path']), "rb") as file:
                        st.download_button(
                            label="⤵️",
                            data=file,
                            file_name=post['image_path'].split("/")[-1],
                            mime="image/jpeg",
                            key=f"download_{post['_id']}"
                        )
                st.divider()

    def view_header(self):
        # Logged in
        if self.get_auth_id():
            st.title(f"Chào mừng {self.get_auth_username()}!")
            st.write("Bạn đã đăng nhập thành công.")
            if st.button("Đăng xuất"):
                self.remove_authentication_info()
                st.rerun()
            if st.button("Đăng ảnh"):
                st.switch_page("pages/upload.py")

        #  Guess mode
        else:
            st.title("Trang chủ")
            if st.button("Đăng ký"):
                st.switch_page("pages/register.py")
            if st.button("Đăng nhập"):
                st.switch_page("pages/login.py")


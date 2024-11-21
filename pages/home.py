import streamlit as st
from bases.page import Page
from repositories.post import post_repository
import os

class HomePage(Page):
    def fetch_data(self, keyword = None, page = 1):
        posts = post_repository.find_all(keyword, page)
        st.session_state.search = keyword
        st.session_state.posts = posts["items"]
        st.session_state.total_pages = posts["total_pages"]
        st.session_state.current_page = posts["current_page"]

    def view(self):
        self.view_header()

        if "posts" not in st.session_state:
            self.fetch_data(keyword=None, page=1)

        [_,_,_,search_input,search_btn] = st.columns([1,1,1,1,0.275], vertical_alignment='bottom')
        with search_input:
            search = st.text_input("Tìm kiếm")
        with search_btn:
            if (st.button("Tìm kiếm")):
                self.fetch_data(search, 1)

        max_columns = 4
        grid_columns = st.columns(max_columns)

        posts = st.session_state.posts
        for index, post in enumerate(posts):
            with grid_columns[index % max_columns]:
                st.image(os.path.abspath(post['image_path']), use_container_width=True)

                st.write(f"**{post['title']}**")
                st.write(post["content"])
                st.write(f"*Đăng bởi: {post['user']['username']}*")

                [download_button, like_button] = st.columns([0.1, 0.9])
                with like_button:
                   if self.get_auth_id():
                        is_liked = self.get_auth_id() in post["likes"]
                        button_label = "💓" if is_liked else "🖤"
                        if st.button(f"{len(post["likes"])} {button_label}", key=f"like_{post['_id']}", ):
                            post_repository.like_post(post["_id"], self.get_auth_id())
                            self.fetch_data(keyword=st.session_state.search, page=st.session_state.current_page)
                            st.rerun()

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

        _, _, previous_col, page_info_col, next_col, _, _ = st.columns([1, 3, 2, 2, 2, 3, 1], vertical_alignment="center")

        if st.session_state.current_page > 1:
            with previous_col:
                if st.button("Trang trước"):
                    self.fetch_data(keyword=st.session_state.search, page=st.session_state.current_page - 1)
                    st.rerun()
        with page_info_col:
            st.write(f"Trang {st.session_state.current_page}/{st.session_state.total_pages}")

        if st.session_state.current_page < st.session_state.total_pages:
            with next_col:
                if st.button("Trang sau"):
                    self.fetch_data(keyword=st.session_state.search, page=st.session_state.current_page + 1)
                    st.rerun()

    def view_header(self):
        [_, header_btn_left, header_btn_right] = st.columns([12, 0.9, 1])

        if self.get_auth_id():
            st.title(f"Chào mừng {self.get_auth_username()}!")
            st.write("Bạn đã đăng nhập thành công.")
            with header_btn_left:
                if st.button("Đăng ảnh"):
                    st.switch_page("pages/upload.py")
            with header_btn_right:
                if st.button("Đăng xuất"):
                    self.remove_authentication_info()
                    st.rerun()
        else:
            st.title("Trang chủ")
            with header_btn_left:
                if st.button("Đăng ký"):
                    st.switch_page("pages/register.py")
            with header_btn_right:
                if st.button("Đăng nhập"):
                    st.switch_page("pages/login.py")


import streamlit as st
from bases.page import Page
import os
from streamlit_tags import st_tags
import uuid
from repositories.post import post_repository
from repositories.user import user_repository

class MyPage(Page):
    def fetch_data(self, keyword = None, page = 1):
        my_post = post_repository.find_all(None, page, 20, Page.get_auth_id())
        print(my_post)
        st.session_state.my_post = my_post["items"]
        st.session_state.total_pages = my_post["total_pages"]
        st.session_state.current_page = my_post["current_page"]

    @st.dialog("Bạn muốn xóa ảnh này?")
    def confirm_delete_dialog(self, id):
        if st.button("Xác nhận"):
            post_repository.delete_post(id)
            self.fetch_data(keyword=st.session_state.search, page=st.session_state.current_page)
            st.toast("Xóa ảnh thành công.")
            st.rerun()

    @st.dialog("Sửa thông tin")
    def update_dialog(self, post):
        title = st.text_input("Tiêu đề", value=post["title"])
        content = st.text_input("Nội dung", value=post["content"])
        keywords = st_tags(
            label='Tag:',
            text='Nhập tags',
            maxtags = 10,
            value=post["keywords"],
            key='keyword_tags')
        is_public = st.checkbox("Công khai", value=post["is_public"])
        if (st.button("Cập nhật")):
            post_repository.update_post(post["_id"], title, content, keywords, is_public)
            self.fetch_data(keyword=st.session_state.search, page=st.session_state.current_page)
            st.toast("Cập nhật ảnh thành công.")
            st.rerun()

    def view(self):
        if "my_post" not in st.session_state:
            self.fetch_data(keyword=None, page=1)

        max_columns = 4
        grid_columns = st.columns(max_columns)

        my_post = st.session_state.my_post
        for index, post in enumerate(my_post):
            with grid_columns[index % max_columns]:
                st.image(os.path.abspath(post['image_path']), use_container_width=True)

                st.write(f"**{post['title']}**")
                st.write(post["content"])

                st.markdown("""
                    <style>
                    .tag {
                        display: inline-block;
                        background-color: #007bff;
                        color: white;
                        padding: 5px 10px;
                        margin: 5px;
                        border-radius: 15px;
                        font-size: 14px;
                    }
                    </style>
                    """, unsafe_allow_html=True)
                tags_html = ""
                for tag in post['keywords']:
                    tags_html += f'<span class="tag">{tag}</span>'

                st.markdown(tags_html, unsafe_allow_html=True)

                [download_button, like_button, delete_button, edit_button] = st.columns([1,1,1,1])
                with like_button:
                    st.button(f"{len(post["likes"])} 💓", key=f"like_{post['_id']}", )
                with download_button:
                    with open(os.path.abspath(post['image_path']), "rb") as file:
                        st.download_button(
                            label="⤵️",
                            data=file,
                            file_name=post['image_path'].split("/")[-1],
                            mime="image/jpeg",
                            key=f"download_{post['_id']}"
                        )
                with delete_button:
                    if st.button("Xóa", key=f"delete_{post['_id']}"):
                        self.confirm_delete_dialog(post['_id'])
                with edit_button:
                    if st.button("Sửa", key=f"edit_{post['_id']}"):
                        self.update_dialog(post)

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

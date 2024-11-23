import streamlit as st
from bases.page import Page
import os
from streamlit_tags import st_tags
import uuid
from repositories.post import post_repository
from repositories.user import user_repository

class UploadPage(Page):
    def store_image(self, image):
        UPLOAD_FOLDER = 'static/uploaded_images'
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)

        unique_name = f"{uuid.uuid4()}_{image.name}"
        image_path = os.path.join(UPLOAD_FOLDER, unique_name)
        with open(image_path, 'wb') as f:
            f.write(image.getbuffer())
        return image_path

    def upload(self, title, content, keywords, is_public, image):
        if (title == "") or (content == "") or (image == None):
            st.error("Vui lòng điền đầy đủ thông tin.")
            return

        image_path = self.store_image(image)

        user = user_repository.find_by_username(self.get_auth_username())

        post_repository.create_post(title, content, keywords, is_public, image_path, user["_id"])

        st.success("Đăng ảnh thành công.")

    def view(self):
        if (self.get_auth_username() == None):
            st.error("Vui lòng đăng nhập để tiếp tục.")
            st.stop

        st.title("Đăng ảnh")
        title = st.text_input("Tiêu đề")
        content = st.text_input("Nội dung")
        keywords = st_tags(
            label='Tag:',
            text='Nhập tags',
            maxtags = 10,
            key='keyword_tags')
        is_public = st.checkbox("Công khai", value=True)
        image = st.file_uploader("Chọn ảnh", accept_multiple_files=False, type=['png', 'jpg', 'jpeg'])

        if st.button("Đăng"):
            self.upload(title, content, keywords, is_public, image)
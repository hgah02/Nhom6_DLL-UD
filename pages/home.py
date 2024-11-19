import streamlit as st
from bases.page import Page
from repositories.post import post_repository

class HomePage(Page):
    def view(self):
        if (self.get_auth()):
            st.title(f"Chào mừng {self.get_auth()}!")
            st.write("Bạn đã đăng nhập thành công.")
            if st.button("Đăng xuất"):
                self.remove_authentication_info()
                st.rerun()
            if st.button("Đăng ảnh"):
                st.switch_page("pages/upload.py")
                st.rerun()
        else:
            st.title("Trang chủ")
            if st.button("Đăng ký"):
                st.switch_page("pages/register.py")
            if st.button("Đăng nhập"):
                st.switch_page("pages/login.py")

        search = st.text_input("Tìm kiếm:")

        with open("css/grid.css") as file:
            css = file.read()

        st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

        divs = [
            f"""
            <div class="mansory_item">
                <div class="content">
                    <img src="app/{post["image_path"]}" />
                </div>
            </div>
            """
            for post in post_repository.find_all()
        ]

        html = """
            <div class="mansory">
            %s
            </div>
        """ % (
            ''.join(divs),
        )

        st.html(html)


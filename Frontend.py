import streamlit as st

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "name" not in st.session_state:
    st.session_state.name = None

if "surname" not in st.session_state:
    st.session_state.surname = None


def login():
    name = st.text_input("Name")
    surname = st.text_input("Surname")
    if st.button("Log in"):
        st.session_state.logged_in = True
        st.session_state.name = name
        st.session_state.surname = surname
        st.rerun()

def logout():
    if st.button("Log out"):
        st.session_state.logged_in = False
        st.rerun()

login_page = st.Page(login, title="Log in", icon=":material/login:")
logout_page = st.Page(logout, title="Log out", icon=":material/logout:")

settings = st.Page("pages/Settings.py", title="Settings", icon=":material/settings:", default=True)
home = st.Page("pages/Home.py", title="Home", icon=":material/home:")
input = st.Page("pages/Input.py", title="Interests", icon=":material/favorite:")
courses = st.Page("pages/Courses.py", title="Courses", icon=":material/list:")
if st.session_state.logged_in:
    pg = st.navigation(
        {
            "Account": [logout_page, settings],
            "General": [home, input, courses],
        }
    )
else:
    pg = st.navigation([login_page])

pg.run()

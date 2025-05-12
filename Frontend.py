import json
import streamlit as st


if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "name" not in st.session_state:
    st.session_state.name = None

if "surname" not in st.session_state:
    st.session_state.surname = None


def login():
    with st.form("Name"):
        name = st.text_input("Name", placeholder="ex: Andrea").strip()
        surname = st.text_input("Surname", placeholder="ex: Calì").strip()
        if st.form_submit_button("Log in") and name and surname:
            user_id = name + "|" + surname
            with open('users.json', 'r', encoding='utf-8') as f:
                users = json.load(f)
            with open('courses.json', 'r', encoding='utf-8') as f:
                courses_titles = [i['title'] for i in json.load(f)]

            st.session_state.id = user_id
            st.session_state.logged_in = True
            st.session_state.name = name
            st.session_state.surname = surname

            if user_id in users.keys():
                user = users[user_id]
                st.session_state.liked_courses = user['liked_courses']
                st.session_state.interests = user['interests']
                st.session_state.interest_courses = [i for i in user['interest_courses'] if i in courses_titles]
            else:
                st.session_state.liked_courses = []
                st.session_state.interests = None
                st.session_state.interest_courses = []
                users[st.session_state.id] = {
                    'id': st.session_state.id,
                    'name': st.session_state.name,
                    'surname': st.session_state.surname,
                    'liked_courses': st.session_state.liked_courses,
                    'interests': st.session_state.interests,
                    'interest_courses': st.session_state.interest_courses
                }
                with open('users.json', 'w', encoding='utf-8') as f:
                    json.dump(users, f, ensure_ascii=False, indent=4)

            st.switch_page(home)
            st.rerun()


def logout():
    st.text("Do you want to log out?")
    if st.button("Yes :("):
        st.session_state.logged_in = False
        with open('users.json', 'r', encoding='utf-8') as f:
            users = json.load(f)
            users[st.session_state.id] = {
                'id': st.session_state.id,
                'name': st.session_state.name,
                'surname': st.session_state.surname,
                'liked_courses': st.session_state.liked_courses,
                'interests': st.session_state.interests,
                'interest_courses': st.session_state.interest_courses
            }
        with open('users.json', 'w', encoding='utf-8') as f:
            json.dump(users, f, ensure_ascii=False, indent=4)

        st.rerun()


login_page = st.Page(login, title="Log in", icon=":material/login:")
logout_page = st.Page(logout, title="Log out", icon=":material/logout:")

settings = st.Page("pages/Settings.py", title="Settings", icon=":material/settings:", default=True)
home = st.Page("pages/Home.py", title="Home", icon=":material/home:")
input_ = st.Page("pages/Input.py", title="Interests", icon=":material/favorite:")
courses = st.Page("pages/Courses.py", title="Courses", icon=":material/list:")
if st.session_state.logged_in:
    pg = st.navigation(
        {
            "Account": [logout_page, settings],
            "General": [home, input_, courses],
        }
    )
else:
    pg = st.navigation([login_page])
pg.run()

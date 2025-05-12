import json
import streamlit as st

st.title("Settings")
with st.form("Change name"):
    st.text("Do you want to change name and surname?")
    name = st.text_input("new name", value=st.session_state.name, placeholder="ex: Andrea").strip()
    surname = st.text_input("new surname", value=st.session_state.surname, placeholder="ex: Calì").strip()
    submitted = st.form_submit_button("Submit")
    if submitted and name and surname:
        st.session_state.name = name
        st.session_state.surname = surname

        with open('users.json', 'r', encoding='utf-8') as f:
            users = json.load(f)
            del users[st.session_state.id]
            st.session_state.id = name + "|" + surname
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

with st.form("Delete account"):
    st.text("Do you want to delete account?(")
    submitted = st.form_submit_button("Yes, delete please")
    if submitted:
        with open('users.json', 'r', encoding='utf-8') as f:
            users = json.load(f)
            del users[st.session_state.id]
        with open('users.json', 'w', encoding='utf-8') as f:
            json.dump(users, f, ensure_ascii=False, indent=4)
        st.session_state.logged_in = False
        st.rerun()

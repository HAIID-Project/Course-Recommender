import json
import streamlit as st

st.title("Settings")
with st.form("Change name"):
    name = st.text_input("Change name").strip()
    surname = st.text_input("Change surname").strip()
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

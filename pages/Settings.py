import streamlit as st
st.title("Settings")
with st.form("Change name"):
    name = st.text_input("Change name")
    surname = st.text_input("Change surname")
    submitted = st.form_submit_button("Submit")
    if submitted:
        st.session_state.name = name 
        st.session_state.surname = surname

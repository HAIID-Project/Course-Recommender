import streamlit as st
if "name" in st.session_state and "surname" in st.session_state:
    st.title(f"Hello, {st.session_state.name} {st.session_state.surname}!")
    st.text("Based on your interests, we recommend the following courses:")
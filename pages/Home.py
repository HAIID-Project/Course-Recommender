import streamlit as st
if "name" in st.session_state and "surname" in st.session_state:
    st.title(f"Hello, {st.session_state.name} {st.session_state.surname}!")
    if "interests" not in st.session_state or st.session_state.interests == None:
        st.text("In order to properly recommend courses, we need a bit of information from you. ")
        with st.form("interest form"):
            interests = st.text_input("What do you want to learn? Feel free to write as much as you need to get the point across.")
            if st.form_submit_button():
                st.session_state.interests = interests
                st.rerun()
    else:
        with st.form("revise interest form"):
            interests = st.text_input("Changed your mind? No worries! You can change your interests here!")
            if st.form_submit_button():
                st.session_state.interests = interests
                st.rerun()
        st.text("Based on your interests, we recommend the following courses:")
        # stuff here, add cards later
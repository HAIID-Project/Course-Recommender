import json
import streamlit as st
# from sentence_transformers.cross_encoder import CrossEncoder


def interest_courses(query):
    # model = CrossEncoder("cross-encoder/stsb-distilroberta-base")
    # with open('courses.json', 'r', encoding='utf-8') as f:
    #     courses = {i["keywords"] + ". " + i["description"]: i for i in json.load(f)}
    # corpus = list(courses.keys())
    #
    # ranks = model.rank(query, corpus)
    interesting_courses = []
    # if ranks[9]['score'] > 0.2:
    #     for rank in ranks:
    #         if rank['score'] < 0.2:
    #             break
    #         interesting_courses.append(courses[corpus[rank['corpus_id']]]['title'])
    # else:
    #     interesting_courses = [courses[corpus[rank['corpus_id']]]['title'] for rank in ranks[:3]]
    # print(interesting_courses)
    return interesting_courses


if "name" in st.session_state and "surname" in st.session_state:

    st.title(f"Hello, {st.session_state.name} {st.session_state.surname}!")

    if "interests" not in st.session_state or st.session_state.interests is None:
        st.text("In order to properly recommend courses, we need a bit of information from you. ")
        with st.form("interest form"):
            interests = st.text_input(
                "What do you want to learn? Feel free to write as much as you need to get the point across.").strip()
            if st.form_submit_button() and interests:
                st.session_state.interests = interests
                st.session_state.interest_courses = interest_courses(interests)
                st.rerun()
    else:

        with st.form("revise interest form"):
            interests = st.text_input("Changed your mind? No worries! You can change your interests here!").strip()
            if st.form_submit_button():
                st.session_state.interests = interests
                if interests:
                    st.session_state.interest_courses = interest_courses(interests)
                else:
                    st.session_state.interest_courses = []
                st.rerun()
        st.text("Based on your interests, we recommend the following courses:")

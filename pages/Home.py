import json
import requests
import streamlit as st
from streamlit_extras.stylable_container import stylable_container

if 'liked_courses' not in st.session_state:
    st.session_state.liked_courses = []

def create_card(title, description, course_type, course_url):
    max_length = 40
    truncated_desc = (description[:max_length] + '...') if len(description) > max_length else description
    truncated_title = (title[:max_length] + '...') if len(title) > max_length else title
    if course_type == "Languages":
        card_color = f"#6886af"
    elif course_type == "Programming":
        card_color = f"#d7adbe"
    elif course_type == "History":
        card_color = f"#ab94b0"
    elif course_type == "Finance":
        card_color = f"#116594"
    elif course_type == "Data":
        card_color = f"#242d62"
    elif course_type == "Medicine":
        card_color = f"#585387"
    elif course_type == "Law":
        card_color = f"#adb7dc"
    elif course_type == "Chemistry":
        card_color = f"#b6c6db"
    elif course_type == "Technology":
        card_color = f"#82465c"
    elif course_type == "Philosophy":
        card_color = f"#c56477"
    else:
        card_color = f"#003f5c"
    is_liked = title in st.session_state.liked_courses
    card_key = f"card_{description}"

    with stylable_container(
            key=f"outer_{card_key}",
            css_styles="""
            {
                border: 1px solid rgba(49, 51, 63, 0.2);
                border-radius: 0.5rem;
                padding: 0;
                margin-bottom: 0;
                overflow: hidden;
                min-height: 180px;
            }
        """
    ):
        card_container = st.container()

        with card_container:
            color_col, content_col = st.columns([1, 2])

            with color_col:
                st.markdown(
                    f'''
                    <div style="background-color: {card_color}; min-height: 180px;">
                        {f'<a href="{course_url}" target="_blank" style="position: absolute; '
                         f'bottom: -8px; left: 8px; background: white; border: none; border-radius: 0.5rem; '
                         f'padding: 0.3em 0.6em; font-size: 0.8em; text-decoration: none; '
                         f'color: {card_color};">🔗 Visit</a>' if course_url else ''}
                    </div>
                    ''',
                    unsafe_allow_html=True
                )

            with content_col:
                with stylable_container(
                        key=f"content_{card_key}",
                        css_styles="""
                        {
                            padding: 8px 12px 0px 12px;
                            min-height: 180px;
                            position: relative;
                        }
                    """
                ):
                    st.markdown(
                        f'<div style="margin-bottom: 8px; padding-bottom: 4px; max-width: 70%;"><strong>{truncated_title}</strong></div>',
                        unsafe_allow_html=True
                    )

                    st.markdown(
                        f'<div style="padding-bottom: 4px; font-size: 13px; max-width: 80%">{truncated_desc}</div>',
                        unsafe_allow_html=True
                    )

                    st.markdown(
                        f'<span style="color: {card_color}; font-size: 0.8em; border: 1px solid {card_color}; '
                        f'border-radius: 0.5rem; padding: 0.2em 0.5em; display: inline-block;">{course_type}</span>',
                        unsafe_allow_html=True
                    )

                    with stylable_container(
                            key=f"button_{card_key}",
                            css_styles="""
                            {
                                position: absolute;
                                bottom: 25px;
                                right: -160px; 
                            }
                        """
                    ):
                        btn_container = st.empty()

                        if btn_container.button(
                                "♥️" if is_liked else "🤍",
                                key=f"like_{description}",
                                help="Like this course"
                        ):
                            if is_liked:
                                st.session_state.liked_courses.remove(title)
                            else:
                                st.session_state.liked_courses.append(title)
                            st.rerun()


def interest_courses(query):
    url = 'http://127.0.0.1:5000/suggest'
    params = {'query': query}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()['interest_courses']
    else:
        return ["Sport Algorithmic Programming", "Philosophy", "Quantum Computing. Less Formulas — More Understanding"]


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

        with open('courses.json', 'r', encoding='utf-8') as f:
            card_data = json.load(f)

        cols = st.columns(2)
        course_counter = 0
        for course_data in card_data:
            if course_data["title"] in st.session_state.interest_courses:
                with cols[course_counter % 2]:
                    create_card(
                        course_data["title"],
                        course_data["description"],
                        course_data["tag"],
                        course_data["link"]
                    )
                course_counter += 1

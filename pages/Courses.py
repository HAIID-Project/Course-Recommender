import json
import streamlit as st
from streamlit_extras.stylable_container import stylable_container


st.title("All courses")

# Initialize session state
if 'selected_theme' not in st.session_state:
    st.session_state.selected_theme = None
if 'liked_courses' not in st.session_state:
    st.session_state.liked_courses = []

theme_options = ["Languages", "Programming", "History", "Finance", "Data",
                 "Medicine", "Law", "Chemistry", "Technology", "Philosophy"]

selected = st.pills(
    "Filter by theme",
    theme_options,
    key='theme_pills'
)

if selected != st.session_state.get('current_pill_selection'):
    st.session_state.current_pill_selection = selected
    st.session_state.selected_theme = selected if selected != st.session_state.selected_theme else None
    st.rerun()

search = st.text_input("Search by name")


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


def create_card_grid(num_columns=2):
    with open('courses.json', 'r', encoding='utf-8') as f:
        card_data = json.load(f)

        filtered_data = card_data

        if st.session_state.selected_theme:
            filtered_data = [course for course in filtered_data
                             if course["tag"] == st.session_state.selected_theme]

        if search:
            search_lower = search.lower()
            filtered_data = [course for course in filtered_data
                             if (search_lower in course["title"].lower() or
                                 search_lower in course["description"].lower())]

        cols = st.columns(num_columns)
        for i, data in enumerate(filtered_data):
            with cols[i % num_columns]:
                create_card(data["title"], data["description"], data["tag"], data["link"])

        if not filtered_data:
            st.warning("No courses match your filters")


with open('users.json', 'r', encoding='utf-8') as f:
    users = json.load(f)
    users[st.session_state.id]['liked_courses'] = st.session_state.liked_courses
with open('users.json', 'w', encoding='utf-8') as f:
    json.dump(users, f, ensure_ascii=False, indent=4)

create_card_grid(num_columns=2)

import streamlit as st

st.title("My Favorite Courses")

if not st.session_state.get('liked_courses'):
    st.warning("You haven't liked any courses yet!")
    st.page_link("pages/Courses.py", label="Browse Courses →")
else:
    # Get all course data (should match what's in Courses.py)
    all_courses = {
        "Project Alpha": {"description": "Advanced analytics platform", "type": "Programming"},
        "Dashboard X": {"description": "Real-time monitoring system", "type": "Programming"},
        "Data Explorer": {"description": "Interactive visualization tool", "type": "Design"},
        "Model Builder": {"description": "Machine learning interface", "type": "Design"},
        "Report Generator": {"description": "Automated PDF reports", "type": "Business"},
        "API Gateway": {"description": "Centralized service access", "type": "Business"}
    }
    
    st.write("### Your liked courses:")
    
    for course_title in st.session_state.liked_courses:
        if course_title in all_courses:
            course = all_courses[course_title]
            with st.expander(f"{course_title} ({course['type']})"):
                st.write(course["description"])
                if st.button(
                    "❌ Remove", 
                    key=f"remove_{course_title}",
                    type="primary"
                ):
                    st.session_state.liked_courses.remove(course_title)
                    st.rerun()
import streamlit as st
from streamlit_pills import pills
from streamlit_extras.stylable_container import stylable_container
import random
def random_color():
    return f"#{random.randint(0, 0xFFFFFF):06x}"
st.title("All courses")
selected = pills("Filter by theme", ["Programming", "Business", "Design"], ["🍀", "🎈", "🌈"])
search = st.text_input("Search by name")
def create_card(title, description):
    # Truncate description if too long
    max_length = 60
    truncated_desc = (description[:max_length] + '...') if len(description) > max_length else description
    card_color = random_color()
    card_html = f"""
    <style>
        .card {{
            display: flex;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            overflow: hidden;
            margin-bottom: 10px;
            height: 165px;
            font-family: sans-serif;
        }}
        .color-side {{
            flex: 1;
            min-width: 40%;
            background-color: {card_color};
        }}
        .content-side {{
            flex: 2;
            padding: 12px 15px;
            background: white;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            background-color: black;
        }}
        .card-title {{
            font-size: 1.1rem;
            font-weight: 600;
            margin: 0;
            line-height: 1.3;
        }}
        .card-description {{
            font-size: 0.85rem;
            color: #555;
            margin: 8px 0 12px 0;
            line-height: 1.4;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }}
        .card-footer {{
            display: flex;
            align-items: center;
        }}
        .like-button {{
            background: white;
            border-radius: 5px;
            cursor: pointer;
            font-size: 1rem;
            color: #ff6b6b;
        }}
    </style>
    <div class="card">
        <div class="color-side"></div>
        <div class="content-side">
            <div>
                <div class="card-title">{title}</div>
                <div class="card-description">{truncated_desc}</div>
            </div>
            <div class="card-footer">
                <button class="like-button">❤️ Like</button>
            </div>
        </div>
    </div>
    """
    return card_html

# Create a grid of cards
def create_card_grid(num_columns=3):
    # Sample data for cards
    card_data = [
        {"title": "Project Alpha", "description": "Advanced analytics platform"},
        {"title": "Dashboard X", "description": "Real-time monitoring system"},
        {"title": "Data Explorer", "description": "Interactive visualization tool"},
        {"title": "Model Builder", "description": "Machine learning interface"},
        {"title": "Report Generator", "description": "Automated PDF reports"},
        {"title": "API Gateway", "description": "Centralized service access"}
    ]
    
    # Create columns
    cols = st.columns(num_columns)
    
    # Place cards in grid
    for i, data in enumerate(card_data):
        with cols[i % num_columns]:
            if search not in data["title"]:
                if search not in data["description"]:
                    continue
            with stylable_container(
                key=f"card_{i}",
                css_styles="""
                {
                    margin-bottom: 1rem;
                }
                """
            ):
                st.markdown(
                    create_card(
                        data["title"],
                        data["description"]
                    ),
                    unsafe_allow_html=True
                )

create_card_grid(num_columns=3)
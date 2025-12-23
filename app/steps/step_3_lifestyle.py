import streamlit as st

from state.navigation import next_step, prev_step
from ui.layout import render_header


def render():
    render_header()

    st.header("Step 3: Lifestyle Preferences")
    st.write(f"Signed in as: **{st.session_state.emailaddress}**")

    req = st.session_state.user_requirements

    # -------------------------------------------------
    # Relational & Social Interaction Preferences
    # -------------------------------------------------

    st.subheader("Relational & Social Interaction Preferences")

    req["contact_with_neighbours"] = st.multiselect(
        "How much social contact do you prefer with neighbours?",
        options=[
            "Very high",
            "Moderate",
            "Low",
            "Only when necessary"
        ],
        default=req.get("contact_with_neighbours", [])
    )

    req["mix_of_household"] = st.multiselect(
        "Importance of a diverse mix of household types",
        options=[
            "Important",
            "Neutral",
            "Not important"
        ],
        default=req.get("mix_of_household", [])
    )

    req["degree_shared_responsibility"] = st.multiselect(
        "Desired degree of shared responsibility",
        options=[
            "Strong commitment; active participation",
            "Moderate involvement",
            "Occasional participation",
            "Minimal involvement"
        ],
        default=req.get("degree_shared_responsibility", [])
    )

    req["frequency_shared_activities"] = st.multiselect(
        "How often would you like shared activities?",
        options=[
            "Daily",
            "Several times a week",
            "Once a week",
            "Occasionally",
            "Rarely"
        ],
        default=req.get("frequency_shared_activities", [])
    )

    req["communal_activities"] = st.multiselect(
        "Which communal activities are important to you? (you may select multiple)",
        options=[
            "Shared meals",
            "Gardening",
            "Childcare",
            "Cultural / Social events",
            "Maintenance work"
        ],
        default=req.get("communal_activities", [])
    )

    # -------------------------------------------------
    # Lifestyle & Practical Needs
    # -------------------------------------------------

    st.subheader("Lifestyle & Practical Needs")

    req["noise_tolerance"] = _importance_slider("Noise tolerance")

    req["pets_preferences"] = st.multiselect(
        "Pets policy",
        options=[
            "Have pets",
            "Want pets",
            "No pets allowed",
            "Allergies"
        ],
        default=req.get("pets_preferences", [])
    )

    req["dietary_restrictions"] = st.selectbox(
        "What are your dietary restrictions (for shared meals)?",
        options=["Vegan","Vegetarian","No restrictions","Other"]
    )

    req["smoking_tolerance"] = st.multiselect(
        "Smoking/vaping tolerance (you may select multiple)",
        options=[
            "Nowhere",
            "In private spaces",
            "In outdoor spaces",
            "In shared spaces"
        ],
        default=req.get("smoking_tolerance", [])
    )

    req["hobbies"] = st.text_area(
        "What are your hobbies and interests?",
        value=req.get("hobbies", ""),
        placeholder="Write here..."
    )

    req["other_requirements"] = st.text_area(
        "Other requirements (optional)",
        value=req.get("other_requirements", ""),
        placeholder="Any special requests or preferences..."
    )

    # -------------------------------------------------
    # Navigation
    # -------------------------------------------------

    col1, col2 = st.columns([7, 1])

    with col1:
        if st.button("← Back"):
            prev_step()

    with col2:
        if st.button("Next →"):
            next_step()


# -------------------------------------------------
# Helpers
# -------------------------------------------------

def _importance_slider(label: str) -> int:
    st.write(label)
    st.markdown(
        """
        <div style="display:flex; justify-content:space-between;
                    font-size:0.85em; color:gray;">
            <span>Very low</span>
            <span>Very high</span>
        </div>
        """,
        unsafe_allow_html=True
    )
    return st.slider("", 1, 5, 3, key=f"{label}_slider")
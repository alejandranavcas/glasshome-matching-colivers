import streamlit as st

from state.navigation import next_step, prev_step
from ui.layout import render_header
from data_access.profiles import save_profile_with_embeddings
from utils.validation import min_length


def render():
    render_header()

    st.header("Step 5: Tell Us About Your Values")
    st.write(f"Signed in as: **{st.session_state.username}**")

    living = st.text_area(
        "Living together",
        value=st.session_state.get("living_together", ""),
        max_chars=500,
    )

    decision = st.text_area(
        "Decision-making and rules",
        value=st.session_state.get("decision_making", ""),
        max_chars=500,
    )

    contribution = st.text_area(
        "Personal contribution",
        value=st.session_state.get("personal_contribution", ""),
        max_chars=500,
    )

    col1, col2 = st.columns([7, 1])

    with col1:
        if st.button("← Back"):
            prev_step()

    with col2:
        if st.button("Find Matches →"):
            if not _validate(living, decision, contribution):
                return

            profile = {
                "username": st.session_state.username,
                **st.session_state.user_requirements,
                **st.session_state.user_personality,
                "living_together": living,
                "decision_making": decision,
                "personal_contribution": contribution,
            }

            save_profile_with_embeddings(profile)
            next_step()



def _validate(*texts) -> bool:
    errors = [
        msg for msg in (
            min_length(texts[0], 50, "Living together"),
            min_length(texts[1], 50, "Decision-making"),
            min_length(texts[2], 50, "Personal contribution"),
        ) if msg
    ]

    if errors:
        st.error("\n".join(errors))
        return False

    return True

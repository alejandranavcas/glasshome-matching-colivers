import streamlit as st

from state.navigation import next_step, prev_step
from ui.layout import render_header
from utils.bfi import BFI_QUESTIONS, compute_personality


def render():
    render_header()

    st.header("Step 4: Personality Traits Questionnaire")
    st.write(f"Signed in as: **{st.session_state.username}**")
    st.write(
        "Indicate how much you agree or disagree with the following statements."
    )

    responses = {}

    for item_num, text in BFI_QUESTIONS.items():
        st.markdown(f"**{item_num}. {text}**")

        st.markdown(
            """
            <div style="display:flex; justify-content:space-between;
                        font-size:0.85em; color:gray;">
                <span>Disagree strongly</span>
                <span>Agree strongly</span>
            </div>
            """,
            unsafe_allow_html=True
        )

        responses[item_num] = st.slider(
            "",
            1,
            5,
            value=st.session_state.get(f"bfi_{item_num}", 3),
            key=f"bfi_{item_num}",
        )

        st.markdown("---")

    col1, col2 = st.columns([7, 1])

    with col1:
        if st.button("← Back"):
            prev_step()

    with col2:
        if st.button("Next →"):
            st.session_state.user_personality = compute_personality(responses)
            next_step()

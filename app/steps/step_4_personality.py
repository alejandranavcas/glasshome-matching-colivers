import streamlit as st

from state.navigation import next_step, prev_step
from utils.bfi import BFI_QUESTIONS, compute_personality
from data_access.personality import save_personality_from_state


def render():
    st.write(f"Signed in as: **{st.session_state.emailaddress}**")
    st.header("Step 4: Personality Traits Questionnaire")
    st.markdown(
        """
        You are about to take a 44-question personality quiz based on the Big Five Inventory (OCEAN) traits.
        It is a way to see what makes you, well… you.
        Some questions might feel a bit similar, but that’s on purpose to make your results more accurate.
        Just answer honestly, take your time, and have fun learning a bit more about yourself!
        Your responses will help us understand your personality traits better and improve community matching.
        """
    )
    st.write("Indicate how much you agree or disagree with the following statements.")

    responses = {}

    items = list(BFI_QUESTIONS.items())
    half = len(items) // 2
    col1_items = items[:half]
    col2_items = items[half:]

    col1, col2 = st.columns(2, gap="large")

    with col1:
        for item_num, text in col1_items:
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

    with col2:
        for item_num, text in col2_items:
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

    col1, col2 = st.columns([7, 1])

    with col1:
        if st.button("← Back"):
            prev_step()

    with col2:
        if st.button("Next →"):
            st.session_state.user_personality = compute_personality(responses)
            save_personality_from_state(st.session_state)
            next_step()

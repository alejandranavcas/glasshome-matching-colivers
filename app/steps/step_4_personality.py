import streamlit as st

from state.navigation import next_step, prev_step
from utils.bfi import BFI_QUESTIONS, compute_personality
from data_access.personality import save_personality_from_state, save_personality_responses_from_state

from ui.layout import render_login_info, render_progress_bar


def render():
    render_login_info()
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
    col_left, col_video, col_right = st.columns([1, 2, 1])
    with col_video:
        st.video("images/video-section-3-personality.mp4")

    st.write("Indicate how much you agree or disagree with the following statements.")

    responses = {}
    items = list(BFI_QUESTIONS.items())
    page_sizes = [7, 7, 6, 6, 6, 6, 6]
    total_pages = len(page_sizes)
    if 'personality_page' not in st.session_state:
        st.session_state['personality_page'] = 0
    page = st.session_state['personality_page']

    # Calculate start and end indices for current page
    start_idx = sum(page_sizes[:page])
    end_idx = start_idx + page_sizes[page]
    page_items = items[start_idx:end_idx]

    for item_num, text in page_items:
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

    col1, col2, col3 = st.columns([2, 6, 2])
    with col1:
        if st.button("← Back"):
            if page > 0:
                st.session_state['personality_page'] -= 1
            else:
                prev_step()
    with col3:
        if st.button("Next →"):
            if page < total_pages - 1:
                st.session_state['personality_page'] += 1
                st.rerun()
            else:
                st.session_state.user_personality = compute_personality({k: st.session_state.get(f"bfi_{k}", 3) for k in BFI_QUESTIONS.keys()})
                save_personality_responses_from_state(st.session_state)
                save_personality_from_state(st.session_state)
                next_step()

    render_progress_bar()

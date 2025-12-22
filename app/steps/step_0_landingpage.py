import streamlit as st
from typing import Optional

from state.navigation import next_step
from data_access.demographics import username_exists
from ui.layout import render_header


def render():
    render_header()

    st.header("Welcome to the Co-Living Compatibility Matcher")

    st.markdown(
        """
        **Discover Yourself. Connect with Others.**

        Unlock deeper insights about your personality, values, and preferences—
        and find your perfect community match.

        - Understand Yourself
        - Connect Meaningfully
        - Build Better Communities

        **Your privacy matters.** Your data is stored securely and never shared
        without your consent.
        """
    )

    st.write("Choose a username to identify yourself in matches.")

    # -----------------------------
    # Input
    # -----------------------------

    username = st.text_input(
        "Username",
        value=st.session_state.username,
        max_chars=30,
        help="Enter a display name (3+ characters)."
    )

    # -----------------------------
    # Navigation
    # -----------------------------

    col1, col2 = st.columns([7, 1])

    with col1:
        if st.button("Quit"):
            st.stop()

    with col2:
        if st.button("Next →"):
            _handle_next(username)


# -----------------------------
# Internal logic
# -----------------------------

def _handle_next(username: Optional[str]):
    # normalize None -> empty string and trim whitespace
    username = (username or "").strip()

    if len(username) < 3:
        st.error("Username must be at least 3 characters.")
        return

    if username_exists(username):
        st.error("That username is already taken. Please choose another.")
        return

    st.session_state.username = username
    next_step()

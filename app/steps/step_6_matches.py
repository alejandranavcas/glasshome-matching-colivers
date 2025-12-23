import streamlit as st

from state.navigation import go_to
from ui.layout import render_header
from utils.matching import find_matches


def render():
    render_header()

    st.header("Your Matches")
    st.write(f"Showing matches for **{st.session_state.emailaddress}**")

    matches = find_matches(st.session_state)

    if matches.empty:
        st.warning("No matches found.")
        if st.button("Start Over"):
            go_to(0)
        return

    st.subheader("Top 3 Compatibility Matches")
    st.dataframe(matches)

    if st.button("Start Over"):
        go_to(0)

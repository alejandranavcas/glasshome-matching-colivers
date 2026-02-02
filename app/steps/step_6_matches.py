import streamlit as st

from state.navigation import go_to
from ui.layout import render_header
from utils.matching import find_matches


def render():
    render_header()

    st.header("Your Matches")
    st.write(f"Showing matches for **{st.session_state.emailaddress}**")

    st.subheader("Your profile data")
    st.write(st.session_state.user_requirements)
    st.write(st.session_state.user_personality)
    st.write(st.session_state.share_personal_feelings)
    st.write(st.session_state.group_disputes)
    st.write(st.session_state.group_decision)
    st.write(st.session_state.mistake_reaction)
    st.write(st.session_state.giving_importance)
    st.write(st.session_state.healthy_environments)
    st.write(st.session_state.you_creative)
    st.write(st.session_state.sharing_unfinished_ideas)
    st.write(st.session_state.working_style)

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

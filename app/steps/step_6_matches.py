import streamlit as st

from state.navigation import go_to
from ui.layout import render_header
from utils.matching import find_matches


def render():
    render_header()

    st.header("Your Matches")
    st.write(f"Showing matches for **{st.session_state.emailaddress}**")

    demo_mode = st.session_state.get("demo_mode", "prod")
    if demo_mode == "sarah":
        col1, col2, col3 = st.columns([1, 3, 1])
        with col2:
            st.image(
                "images/demo-cluster-sarah.png",
                use_container_width=True,
                caption="Sarah — Top compatibility cluster",
            )
        st.write("It describes a woman in her early 30s, working as a graphic designer in Stockholm. She values creativity, community engagement, and sustainable living.")

    elif demo_mode == "tom":
        col1, col2, col3 = st.columns([1, 3, 1])
        with col2:
            st.image(
                "images/demo-cluster-tom.png",
                use_container_width=True,
                caption="Tom — Top compatibility cluster",
            )
        st.write("It describes a man in his early 30s, working as a software developer in Berlin. He values privacy, efficiency, and a quiet living environment.")


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

    # If demo mode, skip matching
    if demo_mode in ("sarah", "tom"):
        if st.button("Start Over"):
            go_to(0)
        return

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

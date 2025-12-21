import streamlit as st
from state.navigation import next_step, prev_step
from data_access.demographics import save_demographics_from_state

def render():
    st.header("Step 1: Demographic Information")
    st.write(f"Signed in as: **{st.session_state.username}**")

    st.session_state.fullname = st.text_input("Full name", st.session_state.fullname)
    st.session_state.birthdate = st.text_input("Birth date", st.session_state.birthdate)
    st.session_state.nationality = st.text_input("Nationality", st.session_state.nationality)
    st.session_state.emailaddress = st.text_input("Email", st.session_state.emailaddress)
    st.session_state.currentaddress = st.text_input("Address", st.session_state.currentaddress)
    st.session_state.householdcomposition = st.text_input(
        "Household composition",
        st.session_state.householdcomposition
    )

    col1, col2 = st.columns([7, 1])
    with col1:
        if st.button("← Back"):
            prev_step()

    with col2:
        if st.button("Next →"):
            save_demographics_from_state(st.session_state)
            next_step()

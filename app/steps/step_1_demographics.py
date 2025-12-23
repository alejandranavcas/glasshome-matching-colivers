import re
import streamlit as st
from typing import Optional
import datetime

from state.navigation import next_step, prev_step
from data_access.demographics import save_demographics_from_state, username_exists

def render():
    st.header("Step 1: Demographic Information")
    st.write("Please provide your contact details and demographics. We need this information to be able to contact you with your results and potential matches.")

    st.session_state.fullname = st.text_input("Full name:", st.session_state.fullname, placeholder="e.g. Jane Doe")
    st.session_state.birthdate = st.date_input("Birth date:", value=st.session_state.birthdate if st.session_state.birthdate else None, min_value=datetime.date(1950, 1, 1), max_value=datetime.date.today())
    st.session_state.nationality = st.text_input("Nationality:", st.session_state.nationality, placeholder="e.g. Swedish")
    st.session_state.emailaddress = st.text_input("Email address:", st.session_state.emailaddress, placeholder="e.g. email@example.com")
    st.session_state.householdcomposition = st.text_input(
        "Household composition",
        st.session_state.householdcomposition
    )

    # -----------------------------
    # Internal logic
    # -----------------------------

    def _handle_next(emailaddress: Optional[str]):
        # normalize None -> empty string and trim whitespace
        emailaddress = (emailaddress or "").strip()

        if not st.session_state.fullname:
            st.error("Please enter your full name.")
            return

        if not st.session_state.birthdate:
            st.error("Please select a valid birth date.")
            return

        # Check email format
        email_pattern = r"^[^\s@]+@[^\s@]+\.[^\s@]+$"
        if not re.match(email_pattern, emailaddress):
            st.error("Please enter a valid email address.")
            return

        if username_exists(emailaddress):
            st.error("That email address already exists. Please input a different one.")
            return

        st.session_state.emailaddress = emailaddress

        save_demographics_from_state(st.session_state)
        next_step()

    # -----------------------------
    # Navigation
    # -----------------------------

    col1, col2 = st.columns([7, 1])
    with col1:
        if st.button("← Back"):
            prev_step()

    with col2:
        if st.button("Next →"):
            _handle_next(st.session_state.emailaddress)

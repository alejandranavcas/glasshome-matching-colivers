import streamlit as st
from data_access.credentials import authenticate_user, create_user

from state.navigation import next_step
from state.navigation import go_to


def render():

    st.header("Log in or sign up")
    st.write(
        "Create an account to save your progress and come back later, "
        "or continue without an account."
    )

    st.info(
        "If you continue without signing up, you will need to complete the survey "
        "in one go because we cannot save your progress."
    )

    login_tab, signup_tab, guest_tab = st.tabs(
        ["Log in", "Sign up", "Continue without account"]
    )

    with login_tab:
        with st.form("login_form"):
            login_email = st.text_input("Email", placeholder="you@example.com")
            login_password = st.text_input("Password", type="password")
            login_submitted = st.form_submit_button("Log in and continue →")

        if login_submitted:
            if not login_email or "@" not in login_email:
                st.warning("Please enter a valid email.")
            elif not login_password:
                st.warning("Please enter your password.")
            else:
                is_authenticated, message = authenticate_user(login_email, login_password)
                if not is_authenticated:
                    st.error(message)
                else:
                    st.session_state.auth_mode = "login"
                    st.session_state.emailaddress = login_email.strip().lower()
                    next_step()

    with signup_tab:
        with st.form("signup_form"):
            signup_email = st.text_input("Email", placeholder="you@example.com")
            signup_password = st.text_input("Create password", type="password")
            signup_confirm_password = st.text_input("Confirm password", type="password")
            signup_submitted = st.form_submit_button("Sign up and continue →")

        if signup_submitted:
            if not signup_email or "@" not in signup_email:
                st.warning("Please enter a valid email.")
            elif not signup_password:
                st.warning("Please create a password.")
            elif len(signup_password) < 8:
                st.warning("Password must be at least 8 characters long.")
            elif signup_password != signup_confirm_password:
                st.warning("Passwords do not match.")
            else:
                user_created, message = create_user(signup_email, signup_password)
                if not user_created:
                    st.error(message)
                else:
                    st.success(message)
                    st.session_state.auth_mode = "signup"
                    st.session_state.emailaddress = signup_email.strip().lower()
                    next_step()

    with guest_tab:
        st.write("Continue as guest if you prefer not to create an account.")
        acknowledged = st.checkbox(
            "I understand I must complete the survey in one go because my progress cannot be saved.",
            key="guest_progress_acknowledged",
        )

        if st.button("Continue as guest →"):
            if not acknowledged:
                st.warning("Please confirm that you understand that your progress cannot be saved.")
            else:
                st.session_state.auth_mode = "guest"
                next_step()

    col_back, _ = st.columns([1, 5])
    with col_back:
        if st.button("← Back"):
            go_to(0)


import streamlit as st
from data_access.credentials import authenticate_user, create_user
from data_access.resume import load_user_progress

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
                    normalized_email = login_email.strip().lower()
                    progress = load_user_progress(normalized_email)

                    st.session_state.auth_mode = "login"
                    st.session_state.emailaddress = normalized_email

                    for key, value in progress["demographics"].items():
                        st.session_state[key] = value

                    if progress["requirements"]:
                        st.session_state.user_requirements.update(progress["requirements"])

                    if progress["personality"]:
                        st.session_state.user_personality.update(progress["personality"])

                    for key, value in progress.get("personality_responses", {}).items():
                        st.session_state[key] = value

                    for key, value in progress["values"].items():
                        st.session_state[key] = value

                    contact_options = ["Only when necessary", "Low", "Moderate", "Very high"]
                    mix_options = ["Not important", "Neutral", "Important"]
                    freq_options = ["Rarely", "Occasionally", "Once a week", "Several times a week", "Daily"]

                    contact_value = st.session_state.user_requirements.get("contact_with_neighbours")
                    if contact_value in contact_options:
                        st.session_state.contact_slider = contact_options.index(contact_value) + 1

                    mix_value = st.session_state.user_requirements.get("mix_of_household")
                    if mix_value in mix_options:
                        st.session_state.mix_slider = mix_options.index(mix_value) + 1

                    freq_value = st.session_state.user_requirements.get("frequency_shared_activities")
                    if freq_value in freq_options:
                        st.session_state.freq_slider = freq_options.index(freq_value) + 1

                    st.session_state["Quiet hours_slider"] = int(
                        st.session_state.user_requirements.get("quiet_hours_importance", 3)
                    )
                    st.session_state["Guest policy_slider"] = int(
                        st.session_state.user_requirements.get("guest_policy_importance", 3)
                    )

                    go_to(progress["resume_step"])

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


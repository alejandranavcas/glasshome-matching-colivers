import streamlit as st

from state.navigation import next_step
from ui.layout import render_header


def render():
    render_header()

    st.header("Welcome to the Co-Living Compatibility Matcher")

    st.markdown(
        """
        **Discover Yourself. Connect with Others.**

        Unlock deeper insights about your personality, values, and preferences,
        and find your perfect community match.

        Our app helps you to:
        """
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        with st.container(border=True):
            st.write("### 🧠 Understand Yourself")
            st.markdown("""**Explore your unique traits and what drives you.**""")
    with col2:
        with st.container(border=True):
            st.write("### 🤝 Connect Meaningfully")
            st.write("""**Meet like-minded individuals who share your values.**""")

    with col3:
        with st.container(border=True):
            st.write("### 🏡 Build Better Communities")
            st.write("""**Create groups that truly fit, not just click.**""")

    st.markdown(
        """
        Start your journey today and see how understanding yourself can transform the way you connect with others.

        After this evaluation you will:
        - Have a profile on our app with specific personalized answers.
        - Be part of our database where we use the profiles to do better matches.
        - Be suggested matching communities and/or individuals.
        """
    )

    st.write("### Structure of the Questionnaire")
    st.markdown(
        """
        The questionnaire is divided into several key sections. Each section is designed to provide insights that contribute to a holistic understanding of who you are and what you seek in a living environment:

        1. **Demographics**: Basic information to help us understand your background and to have your contact details.
        2. **Requirements**: Specify your practical requirements for co-living.
        3. **Lifestyle Preferences**: Share your habits and lifestyle preferences.
        4. **Personality Assessment**: Dive deep into your traits and behaviors.
        5. **Values Exploration**: Identify what matters most to you in a community setting.
        """
    )

    st.divider()

    st.markdown("""**Your privacy matters.**
                Your data is stored securely and never shared
                without your consent."""
                )

    # Checkbox to accept terms
    accept = st.checkbox("I accept [AGB](https://www.glasshome.studio/terms-and-conditions) and data storage.")

    # -----------------------------
    # Navigation
    # -----------------------------

    col1, col2 = st.columns([5, 1])

    with col2:
        if st.button("Start Questionnaire →"):
            if accept:
                next_step()
            else:
                st.warning("Please accept AGB and data storage to continue.")

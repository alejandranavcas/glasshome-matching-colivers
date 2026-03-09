import streamlit as st

def render_header():
    st.image("images/header-option2.jpeg", width="stretch")

def render_login_info():
    demo_mode = st.session_state.get("demo_mode", "prod")

    col1, col2 = st.columns([10, 1])
    with col1:
        st.write(f"Signed in as: **{st.session_state.emailaddress}**")

    with col2:
        if demo_mode == "sarah":
            st.image("images/profile-sarah.jpeg", width=100)

        elif demo_mode == "tom":
            st.image("images/profile-tom.jpeg", width=100)

        else:
            st.image("https://www.gravatar.com/avatar/" + __import__('hashlib').md5(st.session_state.emailaddress.lower().encode()).hexdigest() + "?d=initials&s=40", width=40)

def render_progress_bar():
    """Display a progress bar showing current step out of total steps."""
    # Define sub-steps for each main step
    step_substeps = {
        2: 1,  # demographics
        3: 4,  # practical (4 pages)
        4: 3,  # lifestyle (3 pages)
        5: 7,  # personality (7 pages)
        6: 3,  # values (3 pages)
    }
    survey_start_step = 2
    survey_end_step = 6
    # Calculate total steps
    total_steps = sum(step_substeps.values())

    # Determine current step and sub-step
    main_step = st.session_state.get("step", survey_start_step)
    sub_step = 0
    if main_step == 3:
        sub_step = st.session_state.get("practical_page", 0)
    elif main_step == 4:
        sub_step = st.session_state.get("lifestyle_page", 0)
    elif main_step == 5:
        sub_step = st.session_state.get("personality_page", 0)
    elif main_step == 6:
        sub_step = st.session_state.get("values_page", 0)

    # Calculate display step
    display_step = 1
    for s in range(survey_start_step, main_step):
        display_step += step_substeps.get(s, 1)
    display_step += sub_step
    # Clamp display_step
    display_step = min(display_step, total_steps)
    progress = (display_step - 1) / (total_steps - 1)

    st.markdown("---")
    st.progress(progress)
    st.caption(f"Step {display_step} of {total_steps}")

def render_footer():
    st.markdown("---")
    st.markdown("© 2026 Glasshome. All rights reserved.")

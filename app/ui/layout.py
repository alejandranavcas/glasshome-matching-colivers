import streamlit as st

def render_header():
    st.image("images/header-glasshome.png", width="stretch")
    st.markdown("<h1 style='text-align:center'>Co-Living Compatibility Matching</h1>", unsafe_allow_html=True)

def render_login_info():
    col1, col2 = st.columns([10, 1])
    with col1:
        st.write(f"Signed in as: **{st.session_state.emailaddress}**")
    with col2:
        if st.session_state.get("DEMO_MODE_SARAH"):
            st.image("images/profile-sarah.jpeg", width=100)
        elif st.session_state.get("DEMO_MODE_TOM"):
            st.image("images/profile-tom.jpeg", width=100)
        else:
            st.image("https://www.gravatar.com/avatar/" + __import__('hashlib').md5(st.session_state.emailaddress.lower().encode()).hexdigest() + "?d=initials&s=40", width=40)

def render_progress_bar():
    """Display a progress bar showing current step out of total steps."""
    total_steps = 5  # Adjust based on your total number of steps
    current_step = st.session_state.get("step", 1)

    progress = current_step / total_steps
    st.markdown("---")
    st.progress(progress)
    st.caption(f"Step {current_step} of {total_steps}")

def render_footer():
    st.markdown("---")
    st.markdown("© 2024 Glasshome Collective. All rights reserved.")

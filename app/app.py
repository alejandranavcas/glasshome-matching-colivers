import streamlit as st

from ui_settings import apply_theme
from state.init import init_session_state
from pages import STEP_REGISTRY


def main():
    apply_theme()
    init_session_state()

    step = st.session_state.step

    if step not in STEP_REGISTRY:
        st.error("Invalid application state. Restarting.")
        st.session_state.step = 0
        st.rerun()

    STEP_REGISTRY[step]()


if __name__ == "__main__":
    main()
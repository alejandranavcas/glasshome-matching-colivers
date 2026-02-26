import streamlit as st


def reset_session_state(start_step: int = 0):
	st.session_state.clear()
	st.session_state.step = start_step
	st.rerun()

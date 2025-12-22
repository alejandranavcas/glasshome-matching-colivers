import streamlit as st

def next_step():
    st.session_state.step += 1
    st.rerun()

def prev_step():
    st.session_state.step -= 1
    st.rerun()

def go_to(step: int):
    st.session_state.step = step
    st.rerun()

import streamlit as st

def render_header():
    st.image("images/header-glasshome.png", width="stretch")
    st.markdown("<h1 style='text-align:center'>Co-Living Compatibility Matching</h1>", unsafe_allow_html=True)

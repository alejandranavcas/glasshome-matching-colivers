import streamlit as st

def init_session_state():
    defaults = {
        "step": 0,
        "user_requirements": {},
        "user_personality": {},
        "user_values": "",
        "user_text_embeddings": None,

        # demographics
        "fullname": "",
        "birthdate": "",
        "nationality": "",
        "emailaddress": "",
        "resident_type": "",
        "householdcomposition": "",
    }

    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v
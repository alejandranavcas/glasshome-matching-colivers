import streamlit as st

def apply_theme():
    st.set_page_config(
      page_title="Co-Living Compatibility Matching",
      #layout="wide",  # This makes it take full width # or "centered"
      initial_sidebar_state="collapsed" #"collapsed" or "expanded"
  )

    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;700&family=DM+Mono:wght@500&display=swap');

        :root{
          --button-bg: #3C685B;
          --button-text: #FFFFFF;
          --control-radius: 8px;
          --bg-primary: #FFFFFF;
        }

        .block-container {
            max-width: 100%;
            padding-left: 10rem !important;
            padding-right: 10rem !important;
            background-color: var(--bg-primary);
        }

        h1, h2, h3 {
            font-family: 'DM Sans', sans-serif !important;
            font-weight: 700 !important;
        }

        .stButton > button {
            border-radius: var(--control-radius);
            background-color: var(--button-bg);
            color: var(--button-text);
            border: none;
        }

        .stDownloadButton > button {
            border-radius: var(--control-radius);
            background-color: var(--button-bg);
            color: var(--button-text);
            border: none;
        }

        .stButton > button:hover {
            background-color: #D1DDA6;
        }

        .stDownloadButton > button:hover {
            background-color: #D1DDA6;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


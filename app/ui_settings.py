import streamlit as st

def apply_theme():
    st.set_page_config(
      page_title="Co-Living Compatibility Matching",
      #layout="wide",  # This makes it take full width # or "centered"
      initial_sidebar_state="expanded"
  )

    st.markdown(
        """
        <style>
        /* Load fonts */
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,wght@0,300;0,400;0,700;1,400&family=DM+Mono:wght@500&display=swap');

        :root{
          --button-bg: #8e2d2d;
          --button-text: #f6f2ed;
          --control-radius: 8px;
        }

        .main {
            max-width: 100%;
            margin: 0;
            padding: 0;
        }
        .block-container {
            max-width: 100%;
            padding-left: 15rem;
            padding-right: 15rem;
        }

        /* App base */
        .stApp, .main {
          font-family: 'DM Sans', system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial !important;
          line-height: 1.45;
        }

        /* Headings */
        h1, h2, h3, h4, h5, h6 {
          font-family: 'DM Sans', sans-serif !important;
          font-weight: 700 !important;
          margin: .25em 0 !important;
        }

        h1 {
          font-size: 2.5em !important;
        }

        h2 {
          font-size: 2.0em !important;
        }

        /* Small helper/label rows */
        div[style*="display:flex"][style*="font-size:0.85em"] {
          font-family: 'DM Mono', monospace !important;
          font-weight: 500 !important;
          font-size: 13px !important;
        }

        pre, code {
          font-family: 'DM Mono', monospace !important;
          font-weight: 500 !important;
          font-size: 13px;
        }

        /* Buttons */
        .stButton>button {
          border-radius: var(--control-radius) !important;
          color: var(--button-text) !important;
          background-color: var(--button-bg) !important;
          border: none !important;
        }

        .element-container img {
          max-width: 100% !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


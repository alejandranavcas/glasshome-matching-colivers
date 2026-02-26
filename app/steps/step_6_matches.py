import streamlit as st

from data_access.credentials import set_questionnaire_completed
from state.reset import reset_session_state
from ui.layout import render_header
from utils.matching import find_matches
import plotly.graph_objects as go
import base64
from PIL import Image
from utils.pdf_report import generate_pdf_profile, generate_pdf_matches


def render():
    render_header()

    st.header("Congratulations!")
    st.write(f"You just took the first step towards your future Glasshome. Your personal brochure is cooking and will be delivered to your inbox {st.session_state.emailaddress} soon.")

    user_data = {
        "name": st.session_state.fullname,
        "email": st.session_state.emailaddress,
        "resident_type": st.session_state.resident_type,
        "householdcomposition": st.session_state.householdcomposition,
        "user_requirements": st.session_state.user_requirements,
        "user_personality": st.session_state.user_personality
    }

    st.download_button(
        label="Download My Profile PDF",
        data=generate_pdf_profile(user_data),
        file_name="glasshome_profile.pdf",
        mime="application/pdf"
    )

    demo_mode = st.session_state.get("demo_mode", "prod")

    # Set questionnaire as completed for logged in or signed up users
    auth_mode = st.session_state.get("auth_mode")
    if auth_mode in ("login", "signup") and st.session_state.get("emailaddress"):
        if not st.session_state.get("questionnaire_marked_completed", False):
            set_questionnaire_completed(st.session_state.emailaddress)
            st.session_state.questionnaire_marked_completed = True

    if demo_mode == "sarah":
        st.subheader("Your Matches")
        st.write(f"Showing matches for **{st.session_state.emailaddress}**")
        st.write("Based on your neighborhood profile, you could fit well together with the context and people of this neighborhood!")
        col1, col2, col3 = st.columns([1, 3, 1])
        with col2:
            """
            st.image(
                "images/demo-cluster-sarah.png",
                width='stretch',
                caption="Sarah — Top compatibility cluster",
            )
            """

            # Load your image
            img_path = "images/demo-cluster-sarah.png"
            img = Image.open(img_path)
            img_width, img_height = img.size  # use the actual image size

            # Encode the image to base64
            with open(img_path, "rb") as f:
                img_bytes = f.read()
            img_b64 = base64.b64encode(img_bytes).decode()

            fig = go.Figure()

            # Add image as layout background
            fig.add_layout_image(
                dict(
                    source=f"data:image/png;base64,{img_b64}",
                    xref="x",
                    yref="y",
                    x=0,
                    y=img_height,
                    sizex=img_width,
                    sizey=img_height,
                    sizing="stretch",
                    layer="below"
                )
            )

            # Add invisible point with image in hover
            fig.add_trace(
                go.Scatter(
                    x=[1335],
                    y=[850],
                    mode="markers",
                    marker=dict(size=50, opacity=0),  # invisible marker
                    hovertext="FIND OUT MORE →",
                    hoverinfo="text"
                )
            )

            fig.update_xaxes(showgrid=False, visible=False, range=[0, img_width])
            fig.update_yaxes(showgrid=False, visible=False, range=[0, img_height])
            fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))

            st.plotly_chart(fig)
            st.button("FIND OUT MORE →")

    elif demo_mode == "tom":
        st.subheader("Your Matches")
        st.write(f"Showing matches for **{st.session_state.emailaddress}**")
        st.write("Based on your neighborhood profile, you could fit well together with the context and people of this neighborhood!")
        col1, col2, col3 = st.columns([1, 3, 1])
        with col2:
            """
            st.image(
                "images/demo-cluster-tom.png",
                width='stretch',
                caption="Tom — Top compatibility cluster",
            )
            """

            # Load your image
            img_path = "images/demo-cluster-tom.png"
            img = Image.open(img_path)
            img_width, img_height = img.size  # use the actual image size

            # Encode the image to base64
            with open(img_path, "rb") as f:
                img_bytes = f.read()
            img_b64 = base64.b64encode(img_bytes).decode()

            fig = go.Figure()

            # Add image as layout background
            fig.add_layout_image(
                dict(
                    source=f"data:image/png;base64,{img_b64}",
                    xref="x",
                    yref="y",
                    x=0,
                    y=img_height,
                    sizex=img_width,
                    sizey=img_height,
                    sizing="stretch",
                    layer="below"
                )
            )

            # Add invisible point with image in hover
            fig.add_trace(
                go.Scatter(
                    x=[255],
                    y=[370],
                    mode="markers",
                    marker=dict(size=50, opacity=0),  # invisible marker
                    hovertext="FIND OUT MORE →",
                    hoverinfo="text"
                )
            )

            fig.update_xaxes(showgrid=False, visible=False, range=[0, img_width])
            fig.update_yaxes(showgrid=False, visible=False, range=[0, img_height])
            fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))

            st.plotly_chart(fig)
            st.button("FIND OUT MORE →")

    # If demo mode, skip matching
    if demo_mode in ("sarah", "tom"):
        if st.button("Start Over"):
            reset_session_state()
        return

    # Else, find matches based on user input
    matches = find_matches(st.session_state)
    st.subheader("Your Matches")
    st.write(f"Showing matches for **{st.session_state.emailaddress}**")

    if matches.empty:
        if demo_mode == "dev":
            st.warning("No matches found.")
        if demo_mode == "prod":
            st.write("Your are an early bird and that means we need more people to join our database in order for you to be matched. We are continuously expanding our network of Glasshomes, so keep an eye at your inbox: you will receive an email from us when there is an update!")
    else:
        st.subheader("Top 3 Compatibility Matches")
        st.dataframe(matches)
        st.download_button(
            label="Download My Matches PDF",
            data=generate_pdf_matches(user_data, matches),
            file_name="glasshome_matches.pdf",
            mime="application/pdf"
        )

    if demo_mode == "dev":
        st.subheader("Your profile data")
        st.write(st.session_state.user_requirements)
        st.write(st.session_state.user_personality)
        st.write(st.session_state.share_personal_feelings)
        st.write(st.session_state.group_disputes)
        st.write(st.session_state.group_decision)
        st.write(st.session_state.mistake_reaction)
        st.write(st.session_state.giving_importance)
        st.write(st.session_state.healthy_environments)
        st.write(st.session_state.you_creative)
        st.write(st.session_state.sharing_unfinished_ideas)
        st.write(st.session_state.working_style)

    if st.button("Start Over"):
        reset_session_state()

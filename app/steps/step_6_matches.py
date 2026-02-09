import streamlit as st

from state.navigation import go_to
from ui.layout import render_header
from utils.matching import find_matches
import plotly.graph_objects as go
import base64
from PIL import Image


def render():
    render_header()

    st.header("Your Matches")
    st.write(f"Showing matches for **{st.session_state.emailaddress}**")
    st.write("Based on your neighborhood profile, you could fit well together with this with the context and people of this neighborhood!")

    demo_mode = st.session_state.get("demo_mode", "prod")
    if demo_mode == "sarah":
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

    # If demo mode, skip matching
    if demo_mode in ("sarah", "tom"):
        if st.button("Start Over"):
            go_to(0)
        return

    matches = find_matches(st.session_state)

    if matches.empty:
        st.warning("No matches found.")
        if st.button("Start Over"):
            go_to(0)
        return

    st.subheader("Top 3 Compatibility Matches")
    st.dataframe(matches)

    if st.button("Start Over"):
        go_to(0)

import streamlit as st
import tempfile
import os
from openai import OpenAI
from streamlit_sortables import sort_items

from state.navigation import next_step, prev_step
from data_access.profiles import save_texts_with_embeddings, save_texts_with_embeddings_2
# from utils.validation import min_length

from ui.layout import render_login_info, render_progress_bar

def render():
    render_login_info()
    st.header("Step 5: Tell Us About Your Values")
    col_left, col_video, col_right = st.columns([1, 2, 1])
    with col_video:
        st.video("images/video-placeholder.mp4")

    share_personal_feelings = audio_transcription_input(
        "How would you share personal feelings like fears or joys in a neighborhood?",
        "share_personal_feelings"
    )

    group_disputes = audio_transcription_input(
        "In group disputes, how would you react? How would you like the group to come together?",
        "group_disputes"
    )

    group_decision = audio_transcription_input(
        "Imagine a group has made a decision that does not feel true to you. How would you react?",
        "group_decision"
    )

    mistake_reaction_options = [
        "They give me space to fix the mistake",
        "They show compassion and understanding and support me mentally",
        "They support me in fixing the mistake and support me proactively"
    ]
    mistake_reaction = st.selectbox(
        "When you make a mistake, what reaction from others helps you most?",
        options=mistake_reaction_options,
        index=mistake_reaction_options.index(st.session_state.get("mistake_reaction")) if st.session_state.get("mistake_reaction") in mistake_reaction_options else None
    )

    giving_importance = audio_transcription_input(
        "How important is giving to others to you? Where do you feel this the most?",
        "giving_importance"
    )


    st.write("What environments help you most to live in a healthy, balanced way? Please sort them from most important to least important.")
    options = [
        "Suitable personal living space (nice home)",
        "Surrounded by nature",
        "Access to Art & Culture (museum, cinema, concerts)",
        "Humans (Friends, Family and Peers)",
        "Infrastructure (school, supermarkets, shopping centre, hospital)"
    ]

    saved_healthy_environments = st.session_state.get("healthy_environments", [])
    if isinstance(saved_healthy_environments, list):
        ordered_saved = [item for item in saved_healthy_environments if item in options]
        missing_defaults = [item for item in options if item not in ordered_saved]
        options = ordered_saved + missing_defaults

    healthy_environments = sort_items(
        options,
        key="healthy_sort",
        custom_style=NUMBERED_SORTABLE_STYLE,
    )

    you_creative = audio_transcription_input(
        "Do you see yourself as a creative? In which ways are you expressing your creativity?",
        "you_creative"
    )

    sharing_unfinished_ideas_options = [
        "Very comfortable - I share my ideas before they are ready at any time",
        "Comfortable, but I take some time and effort to make my ideas presentable before sharing",
        "I rather get them to an almost-finished state before I bother others",
        "I usually finish a concept, before presenting an idea to a group. This way everyone can understand what I mean."
    ]
    sharing_unfinished_ideas = st.selectbox(
        "How comfortable are you in sharing ideas before they feel finished?",
        options=sharing_unfinished_ideas_options,
        index=sharing_unfinished_ideas_options.index(st.session_state.get("sharing_unfinished_ideas")) if st.session_state.get("sharing_unfinished_ideas") in sharing_unfinished_ideas_options else None
    )

    working_style_options = [
        "I prefer to work alone and only meet the group to define targets and distribute work (90/10)",
        "I prefer to work alone most of the times, but its good to have some breaks to align (70/30)",
        "I prefer an equal mixture of groupwork and private work. (50/50)",
        "I prefer work together most of the times but its good to have some breathing space between (30/70)",
        "I prefer doing everything together and only split up when its truely necessary"
    ]
    working_style = st.selectbox(
        "Which working style do you prefer?",
        options=working_style_options,
        index=working_style_options.index(st.session_state.get("working_style")) if st.session_state.get("working_style") in working_style_options else None
    )


    # -----------------------------
    # Navigation
    # -----------------------------

    col1, col2 = st.columns([7, 1])

    with col1:
        if st.button("← Back"):
            prev_step()

    with col2:
        if st.button("Find Matches →"):
            profile = {
                "username": st.session_state.emailaddress,
                "share_personal_feelings": share_personal_feelings,
                "group_disputes": group_disputes,
                "group_decision": group_decision,
                "mistake_reaction": mistake_reaction,
                "giving_importance": giving_importance,
                "healthy_environments": healthy_environments,
                "you_creative": you_creative,
                "sharing_unfinished_ideas": sharing_unfinished_ideas,
                "working_style": working_style
            }

            save_texts_with_embeddings_2(profile)
            next_step()

    render_progress_bar()


# -----------------------------
# Helper functions
# -----------------------------

NUMBERED_SORTABLE_STYLE = """
.sortable-component {
    counter-reset: item;
}

.sortable-container-body {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}

.sortable-item {
    width: 100%;
}

.sortable-item::before {
    content: counter(item) ". ";
    counter-increment: item;
    font-weight: 600;
}
"""

def get_openai_client():
    demo_mode = st.session_state.get("demo_mode", "prod")

    if demo_mode in ("sarah", "tom"):
        raise RuntimeError(f"OpenAI disabled in demo mode: {demo_mode}")

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY not set")

    return OpenAI(api_key=api_key)


def audio_transcription_input(question_label, session_key):
    st.write(question_label)
    audio_value = st.audio_input("Record your answer:", key=f"audio_{session_key}")
    if audio_value:
        client = get_openai_client()
        audio_bytes = audio_value.getvalue()
        st.audio(audio_bytes, format="audio/wav")
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
            f.write(audio_bytes)
            audio_path = f.name
        with st.spinner("Transcribing..."):
            with open(audio_path, "rb") as audio_file:
                transcript_resp = client.audio.transcriptions.create(
                    file=audio_file,
                    model="gpt-4o-transcribe"
                )
        transcript_text = transcript_resp.text if hasattr(transcript_resp, "text") else str(transcript_resp)
        st.session_state[session_key] = transcript_text
        try:
            os.remove(audio_path)
        except OSError:
            pass
    if st.session_state.get(session_key):
        st.markdown('<span style="color:blue">Transcription: </span>', unsafe_allow_html=True)
        st.markdown(f'<span style="color:blue">{st.session_state[session_key]}</span>', unsafe_allow_html=True)
    return st.session_state.get(session_key, "")

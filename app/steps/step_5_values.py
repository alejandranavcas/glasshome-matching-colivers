import streamlit as st
import tempfile
import os
from openai import OpenAI
from streamlit_sortables import sort_items

from state.navigation import next_step, prev_step
from data_access.profiles import save_profile_with_embeddings
# from utils.validation import min_length

def render():
    st.write(f"Signed in as: **{st.session_state.emailaddress}**")
    st.header("Step 5: Tell Us About Your Values")

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

    mistake_reaction = st.selectbox(
        "When you make a mistake, what reaction from others helps you most?",
        options=[
            "They give me space to fix the mistake",
            "They show compassion and understanding and support me mentally",
            "They support me in fixing the mistake and support me proactively"
        ],
        index=None
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

    healthy_environments = sort_items(options, key="healthy_sort")

    you_creative = audio_transcription_input(
        "Do you see yourself as a creative? In which ways are you expressing your creativity?",
        "you_creative"
    )

    sharing_unfinished_ideas = st.selectbox(
        "How comfortable are you in sharing ideas before they feel finished?",
        options=[
            "Very comfortable - I share my ideas before they are ready at any time",
            "Comfortable, but I take some time and effort to make my ideas presentable before sharing",
            "I rather get them to an almost-finished state before I bother others",
            "I usually finish a concept, before presenting an idea to a group. This way everyone can understand what I mean."
        ],
        index=None
    )

    working_style = st.selectbox(
        "Which working style do you prefer?",
        options=[
            "I prefer to work alone and only meet the group to define targets and distribute work (90/10)",
            "I prefer to work alone most of the times, but its good to have some breaks to align (70/30)",
            "I prefer an equal mixture of groupwork and private work. (50/50)",
            "I prefer work together most of the times but its good to have some breathing space between (30/70)",
            "I prefer doing everything together and only split up when its truely necessary"
        ],
        index=None
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
                "username": st.session_state.username,
                **st.session_state.user_requirements,
                **st.session_state.user_personality,
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

            save_profile_with_embeddings(profile)
            next_step()


# -----------------------------
# Helper functions
# -----------------------------
MY_API_KEY = ""
client = OpenAI(api_key=MY_API_KEY)

def audio_transcription_input(question_label, session_key):
    st.write(question_label)
    audio_value = st.audio_input("Record your answer:", key=f"audio_{session_key}")
    if audio_value:
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
        st.subheader("📝 Transcription")
        st.write(st.session_state[session_key])
    return st.session_state.get(session_key, "")

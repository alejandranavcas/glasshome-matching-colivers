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
    if 'values_page' not in st.session_state:
        st.session_state['values_page'] = 0
    page = st.session_state['values_page']

    # Page 0: Title and video
    if page == 0:
        st.header("Step 5: Tell Us About Your Values")
        col_left, col_video, col_right = st.columns([1, 2, 1])
        with col_video:
            st.video("images/video-section-4-values.mov")

    # Page 1: First set of questions
    if page == 1:
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
        mistake_reaction_options = ["-- Select an option --",
            "They give me space to fix the mistake",
            "They show compassion and understanding and support me mentally",
            "They support me in fixing the mistake and support me proactively"
        ]
        mistake_reaction_value = st.session_state.get("mistake_reaction")
        if not isinstance(mistake_reaction_value, str):
            mistake_reaction_value = ""
        if mistake_reaction_value in mistake_reaction_options:
            idx = mistake_reaction_options.index(mistake_reaction_value)
        else:
            idx = 0
        mistake_reaction = st.selectbox(
            "When you make a mistake, what reaction from others helps you most?",
            options=mistake_reaction_options,
            index=idx
        )
        if mistake_reaction != mistake_reaction_options[0]:
            st.session_state["mistake_reaction"] = mistake_reaction
        else:
            st.session_state["mistake_reaction"] = ""

    # Page 2: Remaining questions
    if page == 2:
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
        st.session_state["healthy_environments"] = healthy_environments
        you_creative = audio_transcription_input(
            "Do you see yourself as a creative? In which ways are you expressing your creativity?",
            "you_creative"
        )
        sharing_unfinished_ideas_options = ["-- Select an option --",
            "Very comfortable - I share my ideas before they are ready at any time",
            "Comfortable, but I take some time and effort to make my ideas presentable before sharing",
            "I rather get them to an almost-finished state before I bother others",
            "I usually finish a concept, before presenting an idea to a group. This way everyone can understand what I mean."
        ]
        sharing_unfinished_ideas_value = st.session_state.get("sharing_unfinished_ideas")
        if not isinstance(sharing_unfinished_ideas_value, str):
            sharing_unfinished_ideas_value = ""
        if sharing_unfinished_ideas_value in sharing_unfinished_ideas_options:
            idx = sharing_unfinished_ideas_options.index(sharing_unfinished_ideas_value)
        else:
            idx = 0
        sharing_unfinished_ideas = st.selectbox(
            "How comfortable are you in sharing ideas before they feel finished?",
            options=sharing_unfinished_ideas_options,
            index=idx
        )
        if sharing_unfinished_ideas != sharing_unfinished_ideas_options[0]:
            st.session_state["sharing_unfinished_ideas"] = sharing_unfinished_ideas
        else:
            st.session_state["sharing_unfinished_ideas"] = ""
        working_style_options = ["-- Select an option --",
            "I prefer to work alone and only meet the group to define targets and distribute work (90/10)",
            "I prefer to work alone most of the times, but its good to have some breaks to align (70/30)",
            "I prefer an equal mixture of groupwork and private work. (50/50)",
            "I prefer work together most of the times but its good to have some breathing space between (30/70)",
            "I prefer doing everything together and only split up when its truely necessary"
        ]
        working_style_value = st.session_state.get("working_style")
        if not isinstance(working_style_value, str):
            working_style_value = ""
        if working_style_value in working_style_options:
            idx = working_style_options.index(working_style_value)
        else:
            idx = 0
        working_style = st.selectbox(
            "Which working style do you prefer?",
            options=working_style_options,
            index=idx
        )
        if working_style != working_style_options[0]:
            st.session_state["working_style"] = working_style
        else:
            st.session_state["working_style"] = ""

    # Navigation
    col1, col2 = st.columns([7, 1])
    with col1:
        if st.button("← Back"):
            if page > 0:
                st.session_state['values_page'] -= 1
            else:
                prev_step()

    def validate_values_page(page):
        if page == 1:
            required = [
                st.session_state.get("share_personal_feelings"),
                st.session_state.get("group_disputes"),
                st.session_state.get("group_decision"),
                st.session_state.get("mistake_reaction"),
            ]
            return all(x is not None and x != "" for x in required)
        elif page == 2:
            required = [
                st.session_state.get("giving_importance"),
                st.session_state.get("healthy_environments"),
                st.session_state.get("you_creative"),
                st.session_state.get("sharing_unfinished_ideas"),
                st.session_state.get("working_style"),
            ]
            # healthy_environments must be a non-empty list
            healthy_envs = st.session_state.get("healthy_environments")
            if not healthy_envs or not isinstance(healthy_envs, list) or len(healthy_envs) == 0:
                return False
            return all(x is not None and x != "" for x in required if not isinstance(x, list))
        return True

    with col2:
        if page == 2:
            if st.button("Find Matches →"):
                if validate_values_page(page):
                    profile = {
                        "username": st.session_state.emailaddress,
                        "share_personal_feelings": st.session_state.get("share_personal_feelings", ""),
                        "group_disputes": st.session_state.get("group_disputes", ""),
                        "group_decision": st.session_state.get("group_decision", ""),
                        "mistake_reaction": st.session_state.get("mistake_reaction", ""),
                        "giving_importance": st.session_state.get("giving_importance", ""),
                        "healthy_environments": st.session_state.get("healthy_environments", []),
                        "you_creative": st.session_state.get("you_creative", ""),
                        "sharing_unfinished_ideas": st.session_state.get("sharing_unfinished_ideas", ""),
                        "working_style": st.session_state.get("working_style", "")
                    }
                    save_texts_with_embeddings_2(profile)
                    next_step()
                else:
                    st.warning("Please fill in all required fields before continuing.")
        else:
            if st.button("Next →"):
                if validate_values_page(page):
                    st.session_state['values_page'] += 1
                    st.rerun()
                else:
                    st.warning("Please fill in all required fields before continuing.")
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

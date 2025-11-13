import streamlit as st
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Initialize session state variables
if 'step' not in st.session_state:
    st.session_state.step = 0  # start at step 0 for username
if 'user_responses' not in st.session_state:
    st.session_state.user_responses = {}
if 'user_description' not in st.session_state:
    st.session_state.user_description = ""
if 'username' not in st.session_state:
    st.session_state.username = ""

# Move questions dictionary to top level scope
questions = {
    "social_orientation": [
        "I prefer making decisions that benefit the group rather than just myself.",
        "Living with others helps me grow as a person.",
        "I enjoy contributing to the success of a community.",
        "I value having my own space more than shared experiences. (reverse)"
    ],
    "community_engagement": [
        "I enjoy participating in shared meals, events, or projects.",
        "I feel comfortable depending on others for small favors.",
        "Being part of a supportive community is important to me.",
        "I like to know my neighbors well."
    ],
    "conflict_openness": [
        "I’m comfortable discussing conflicts openly.",
        "I prefer to avoid confrontation, even if issues remain unresolved. (reverse)",
        "I believe differences of opinion can strengthen relationships."
    ],
    "shared_responsibility": [
        "I believe everyone should share chores equally.",
        "I take initiative to solve shared household problems.",
        "I enjoy planning and organizing group activities."
    ],
    "sustainability_values": [
        "I prefer eco-friendly or minimalist lifestyles.",
        "I’m willing to pay more for sustainable living solutions.",
        "Sharing resources (e.g., tools, appliances) is efficient and fulfilling."
    ],
    "privacy_needs": [
        "I need daily time alone to recharge.",
        "I’m comfortable sharing common spaces most of the time. (reverse)",
        "Having clear boundaries is essential for harmonious living."
    ],
    "diversity_openness": [
        "I enjoy living with people from different cultural backgrounds.",
        "Diversity makes communities stronger.",
        "I’m open to learning from people with different lifestyles or beliefs."
    ]
}

st.title("Co-Living Compatibility Matching POC")

# --- STEP 0: USERNAME ---
if st.session_state.step == 0:
    st.header("Welcome — Create a Username")
    st.write("Choose a username to identify yourself in matches.")

    username = st.text_input("Username", value=st.session_state.username, max_chars=30,
                             help="Enter a display name (3+ characters).")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Quit", key="quit_button"):
            st.stop()
    with col2:
        # Use a single button call and inspect its boolean return value.
        next_clicked = st.button("Next", key="username_next")
        if next_clicked:
            if len(username.strip()) >= 3:
                st.session_state.username = username.strip()
                st.session_state.step = 1
                st.rerun()
            else:
                st.error("Username must be at least 3 characters.")

# --- STEP 1: QUESTIONNAIRE ---
elif st.session_state.step == 1:
    st.header("Step 1: Complete Your Attitudinal Questionnaire")

    st.write(f"Signed in as: **{st.session_state.username}**")

    user_responses = {}
    submit_step1 = False

    # Loop through each domain and collect user responses
    for domain, qs in questions.items():
        st.subheader(domain.replace("_", " ").title())
        domain_scores = []
        for q in qs:
            score = st.slider(q, 1, 5, 3)
            if "(reverse)" in q:
                score = 6 - score
            domain_scores.append(score)
        user_responses[domain] = sum(domain_scores)/len(domain_scores)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back", key="back_to_username"):
            st.session_state.step = 0
            st.rerun()

    with col2:
        if st.button("Next Step", key="next_to_description"):
            st.session_state.user_responses = user_responses
            st.session_state.step = 2
            st.rerun()

# --- STEP 2: FREE TEXT DESCRIPTION ---
elif st.session_state.step == 2:
    st.header("Step 2: Tell Us About Yourself")

    st.write("Please describe yourself, your lifestyle, and what you're looking for in a co-living situation:")
    description = st.text_area("Your Description",
                             help="Write at least 50 characters",
                             max_chars=500)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back", key="back_to_questionnaire"):
            st.session_state.step = 1
            st.rerun()

    with col2:
        if st.button("Find Matches →", key="find_matches"):
            if len(description) >= 50:
                st.session_state.user_description = description
                st.session_state.step = 3
                st.rerun()
            else:
                st.error("Please write at least 50 characters.")

# --- STEP 3: SHOW MATCHES ---
else:
    st.header("Step 3: Your Matches")

    # Load profiles
    profiles_df = pd.read_csv("../data/profiles.csv")

    # Calculate value-based similarity
    user_vector = np.array([float(st.session_state.user_responses[domain])
                           for domain in questions.keys()])
    profile_vectors = profiles_df[list(questions.keys())].astype(float).values
    value_similarities = cosine_similarity(user_vector.reshape(1, -1), profile_vectors)[0]

    # Text similarity placeholder (you'll need to add text descriptions to profiles.csv)
    # For now, we'll just use value-based matching

    profiles_df["similarity"] = value_similarities
    top_matches = profiles_df.sort_values(by="similarity", ascending=False).head(3)

    st.write("## 🧩 Your Top 3 Compatibility Matches")
    st.write(f"Showing matches for **{st.session_state.username}**")
    st.dataframe(top_matches[["user_id", "name", "similarity"]])
    st.bar_chart(top_matches.set_index("name")["similarity"])

    if st.button("Start Over", key="start_over"):
        st.session_state.step = 0
        st.session_state.user_responses = {}
        st.session_state.user_description = ""
        st.session_state.username = ""
        st.rerun()
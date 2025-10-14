import streamlit as st
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# --- PAGE SETUP ---
st.title("Co-Living Compatibility Matching POC")

# --- STEP 1: QUESTIONNAIRE ---
# (All the question + response collection code goes here)
# The part that defines `questions`, loops through them, and builds `user_responses`
st.header("Step 1: Complete Your Attitudinal Questionnaire")

# Domain questions
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

user_responses = {}

# Loop through each domain and collect user responses
for domain, qs in questions.items():
    st.subheader(domain.replace("_", " ").title())
    domain_scores = []
    for q in qs:
        score = st.slider(q, 1, 5, 3)
        # Reverse-code if question contains "(reverse)"
        if "(reverse)" in q:
            score = 6 - score
        domain_scores.append(score)
    # Average score for domain
    user_responses[domain] = sum(domain_scores)/len(domain_scores)

# --- STEP 2: DISPLAY USER PROFILE ---
st.write("Your attitudinal profile:")
st.json(user_responses)

# --- STEP 3: LOAD EXISTING PROFILES ---
profiles_df = pd.read_csv("profiles.csv")

# --- STEP 4: COMPUTE SIMILARITY ---
user_vector = np.array([float(user_responses[domain]) for domain in questions.keys()])
profile_vectors = profiles_df[list(questions.keys())].astype(float).values
similarities = cosine_similarity(user_vector.reshape(1, -1), profile_vectors)[0]
profiles_df["similarity"] = similarities

# --- STEP 5: SHOW MATCHES ---
top_matches = profiles_df.sort_values(by="similarity", ascending=False).head(3)

st.write("## 🧩 Your Top 3 Compatibility Matches")
st.dataframe(top_matches[["user_id", "similarity"]])

st.bar_chart(top_matches.set_index("user_id")["similarity"])

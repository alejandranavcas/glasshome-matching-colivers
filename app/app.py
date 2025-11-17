import streamlit as st
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import os
from datetime import datetime

# Initialize session state variables
if 'step' not in st.session_state:
    st.session_state.step = 0  # start at step 0 for username
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'user_requirements' not in st.session_state:
    st.session_state.user_requirements = {}
if 'user_personality' not in st.session_state:
    st.session_state.user_personality = {}
if 'user_values' not in st.session_state:
    st.session_state.user_values = ""

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
    ]
}

st.image("images/header-glasshome.png", width='stretch')
st.title("Co-Living Compatibility Matching POC")

# --- STEP 0: USERNAME ---
if st.session_state.step == 0:
    st.header("Welcome — Create a Username")
    st.markdown("""Discover Yourself. Connect with Others.

Unlock deeper insights about your personality, values, and preferences—and find your perfect community match.

Our app helps you:
- Understand Yourself: Explore your unique traits and what drives you.
- Connect Meaningfully: Meet like-minded individuals who share your values.
- Build Better Communities: Create groups that truly fit, not just click.

Start your journey today and see how understanding yourself can transform the way you connect with others.


Your Privacy Matters: All your data is securely stored in our private databases and never shared without your consent. You are in control of your information at every step.
    """)
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


# --- STEP 1: LIFESTYLE PREFERENCES ---
elif st.session_state.step == 1:
    st.header("Step 1: Lifestyle Preferences")

    st.write(f"Signed in as: **{st.session_state.username}**")

    # Cleanliness standard
    cleanliness = st.radio(
        "Choose your cleanliness standard:",
        ("Very tidy", "Tidy", "Relaxed"),
        index=1,
        key="cleanliness"
    )

    # Smoking/vaping preference
    smoking = st.radio(
        "Smoking/Vaping preference:",
        ("Yes", "Only in private room", "No"),
        index=2,
        key="smoking"
    )

    # Cats and dogs policy
    pets = st.radio(
        "Pets policy:",
        ("Yes", "Only in private space", "No"),
        index=2,
        key="pets"
    )

    # Desired Location
    desired_location = st.text_input(
        "Desired location (city, neighborhood, or region):",
        placeholder="e.g., Germany, Berlin, Kreuzberg",
        key="desired_location"
    )

    # Other Requirements
    other_requirements = st.text_area(
        "Other requirements (optional):",
        placeholder="Any special requests or preferences...",
        key="other_requirements"
    )

    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back", key="back_to_username_from_lifestyle"):
            st.session_state.step = 0
            st.rerun()

    with col2:
        if st.button("Next Step", key="next_to_questionnaire"):
            if not desired_location.strip():  # Check if the input is empty or only whitespace
                st.warning("Please enter your desired location before proceeding.")
            else:
                st.session_state.user_requirements["cleanliness"] = cleanliness
                st.session_state.user_requirements["smoking"] = smoking
                st.session_state.user_requirements["pets"] = pets
                st.session_state.user_requirements["desired_location"] = desired_location
                st.session_state.user_requirements["other_requirements"] = other_requirements
                st.session_state.step = 2  # Proceed to questionnaire
                st.rerun()


# --- STEP 2: QUESTIONNAIRE ---
elif st.session_state.step == 2:
    st.header("Step 2: Complete Your Attitudinal Questionnaire")

    st.write(f"Signed in as: **{st.session_state.username}**")

    user_personality = {}
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
        user_personality[domain] = sum(domain_scores)/len(domain_scores)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back", key="back_to_lifestyle"):
            st.session_state.step = 1
            st.rerun()

    with col2:
        if st.button("Next Step", key="next_to_description"):
            st.session_state.user_personality = user_personality
            st.session_state.step = 3
            st.rerun()

# --- STEP 3: FREE TEXT DESCRIPTION ---
elif st.session_state.step == 3:
    st.header("Step 3: Tell Us About Your Values")

    st.write("Please describe yourself, your lifestyle, and what you're looking for in a co-living situation:")

    # Three separate prompts
    st.markdown("**Living together**: Imagine you’re living in a shared community or co-housing project. What matters most to you in how people live together?")
    living_together = st.text_area(
        "",
        help="Please write at least 50 characters.",
        max_chars=500,
        key="living_together"
    )

    st.markdown("**Decision-making and rules**: When the group needs to make decisions or set rules, what do you think is the best way to do that?")
    decision_making = st.text_area(
        "",
        help="Please write at least 50 characters.",
        max_chars=500,
        key="decision_making"
    )

    st.markdown("**Personal contribution**: What would you most like to contribute or receive in a community like this?")
    personal_contribution = st.text_area(
        "",
        help="Please write at least 50 characters.",
        max_chars=500,
        key="personal_contribution"
    )

    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back", key="back_to_questionnaire"):
            st.session_state.step = 2
            st.rerun()

    with col2:
        if st.button("Find Matches →", key="find_matches"):

            # Individual 50-character minimum check
            errors = []
            if len(living_together.strip()) < 50:
                errors.append("Living together description must be at least 50 characters.")
            if len(decision_making.strip()) < 50:
                errors.append("Decision-making description must be at least 50 characters.")
            if len(personal_contribution.strip()) < 50:
                errors.append("Personal contribution description must be at least 50 characters.")

            if errors:
                st.error("Please fix the following before continuing:\n" + "\n".join(errors))
            else:
                # Save + continue if valid
                try:
                    save_path = os.path.join("..", "data", "save_mock_profiles.csv")
                    row = {
                        "timestamp": datetime.utcnow().isoformat(),
                        "username": st.session_state.username,
                        "cleanliness": st.session_state.user_requirements.get("cleanliness"),
                        "smoking": st.session_state.user_requirements.get("smoking"),
                        "pets": st.session_state.user_requirements.get("pets"),
                        "desired_location": st.session_state.user_requirements.get("desired_location"),
                        "other_requirements": st.session_state.user_requirements.get("other_requirements"),
                        "living_together": living_together,
                        "decision_making": decision_making,
                        "personal_contribution": personal_contribution
                    }
                    row.update({k: float(v) for k, v in st.session_state.user_personality.items()})
                    pd.DataFrame([row]).to_csv(save_path, mode="a",
                                              header=not os.path.exists(save_path), index=False)

                except Exception as e:
                    st.error(f"Failed to save profile: {e}")

                st.session_state.user_values = "\n\n".join([
                    f"Living together: {living_together}",
                    f"Decision-making: {decision_making}",
                    f"Personal contribution: {personal_contribution}"
                ])
                st.session_state.step = 4
                st.rerun()

# --- STEP 4: SHOW MATCHES ---
else:
    st.header("Step 4: Your Matches")

    # Load profiles
    profiles_df = pd.read_csv("../data/profiles.csv")

    # Calculate value-based similarity
    user_vector = np.array([float(st.session_state.user_personality[domain])
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
        st.session_state.user_personality = {}
        st.session_state.user_values = ""
        st.session_state.username = ""
        st.rerun()
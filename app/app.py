import streamlit as st
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import os
from datetime import datetime
import ast
import json

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

# --- New: initialize demographic fields so text_input(value=...) is safe ---
if 'fullname' not in st.session_state:
    st.session_state.fullname = ""
if 'birthdate' not in st.session_state:
    st.session_state.birthdate = ""
if 'nationality' not in st.session_state:
    st.session_state.nationality = ""
if 'emailaddress' not in st.session_state:
    st.session_state.emailaddress = ""
if 'currentaddress' not in st.session_state:
    st.session_state.currentaddress = ""
if 'householdcomposition' not in st.session_state:
    st.session_state.householdcomposition = ""

# Move questions dictionary to top level scope
bfi_questions = {
    1: "I am talkative",
    2: "I tend to find fault with others",
    3: "I do a thorough job",
    4: "I am depressed, blue",
    5: "I am original, comes up with new ideas",
    6: "I am reserved",
    7: "I am helpful and unselfish with others",
    8: "I can be somewhat careless",
    9: "I am relaxed, handles stress well",
    10: "I am curious about many different things",
    11: "I am full of energy",
    12: "I start quarrels with others",
    13: "I am a reliable worker",
    14: "I can be tense",
    15: "I am ingenious, a deep thinker",
    16: "I generates a lot of enthusiasm",
    17: "I have a forgiving nature",
    18: "I tend to be disorganized",
    19: "I worry a lot",
    20: "I have an active imagination",
    21: "I tend to be quiet",
    22: "I am generally trusting",
    23: "I tend to be lazy",
    24: "I am emotionally stable, not easily upset",
    25: "I am inventive",
    26: "I have an assertive personality",
    27: "I can be cold and aloof",
    28: "I persevere until the task is finished",
    29: "I can be moody",
    30: "I value artistic, aesthetic experiences",
    31: "I am sometimes shy, inhibited",
    32: "I am considerate and kind to almost everyone",
    33: "I do things efficiently",
    34: "I remain calm in tense situations",
    35: "I prefer work that is routine",
    36: "I am outgoing, sociable",
    37: "I am sometimes rude to others",
    38: "I make plans and follow through with them",
    39: "I get nervous easily",
    40: "I like to reflect, play with ideas",
    41: "I have few artistic interests",
    42: "I like to cooperate with others",
    43: "I am easily distracted",
    44: "I am sophisticated in art, music, or literature"
}

bfi_scoring = {
    "extraversion":       [1, 6, 11, 16, 21, 26, 31, 36],
    "agreeableness":      [2, 7, 12, 17, 22, 27, 32, 37, 42],
    "conscientiousness":  [3, 8, 13, 18, 23, 28, 33, 38, 43],
    "neuroticism":        [4, 9, 14, 19, 24, 29, 34, 39],
    "openness":           [5, 10, 15, 20, 25, 30, 35, 40, 41, 44]
}

reverse_items = {2, 6, 8, 9, 12, 18, 21, 23, 24, 27, 31, 34, 35, 37, 41, 43}

### STREAMLIT APP

st.image("images/header-glasshome.png", width='stretch')
st.title("Co-Living Compatibility Matching")

# --- STEP 0: USERNAME ---
if st.session_state.step == 0:
    st.header("Welcome to the Co-Living Compatibility Matcher.")
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
                # Check uniqueness against saved demographics CSV
                try:
                    demo_path = os.path.join("..", "data", "mock_profiles_demographics.csv")
                    if os.path.exists(demo_path):
                        df_demo = pd.read_csv(demo_path, usecols=["username"])
                        # case-insensitive comparison
                        existing = df_demo["username"].astype(str).str.lower().tolist()
                        if username.strip().lower() in existing:
                            st.error("That username is already taken. Please choose a unique username.")
                            # do not advance
                            pass
                        else:
                            st.session_state.username = username.strip()
                            st.session_state.step = 1
                            st.rerun()
                    else:
                        st.session_state.username = username.strip()
                        st.session_state.step = 1
                        st.rerun()
                except Exception as e:
                    st.error(f"Failed to validate username uniqueness: {e}")
            else:
                st.error("Username must be at least 3 characters.")


# --- STEP 1: DEMOGRAPHICS ---
elif st.session_state.step == 1:
    st.header("Step 1: Demographic Information")

    st.write(f"Signed in as: **{st.session_state.username}**")

    st.write("Please provide your contact details and demographics. We need this information to save your profile and filter when the matchmaking happens.")

    fullname = st.text_input("Full name:", value=st.session_state.fullname, max_chars=50,
                             help="Enter your full name.")
    birthdate = st.text_input("Birth date:", value=st.session_state.birthdate, max_chars=10,
                             help="Enter your birthdate (DD/MM/YYYY).")
    nationality = st.text_input("Nationality:", value=st.session_state.nationality, max_chars=30,
                             help="Enter your nationality.")
    emailaddress = st.text_input("Email address:", value=st.session_state.emailaddress, max_chars=50,
                             help="Enter your email address.")
    currentaddress = st.text_input("Current home address:", value=st.session_state.currentaddress, max_chars=100,
                             help="Enter your current home address.")
    householdcomposition = st.text_input("Household composition:", value=st.session_state.householdcomposition, max_chars=100,
                             help="Enter your household composition (e.g., living alone, with family, roommates).")



    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back", key="back_to_welcome_from_demographics"):
            st.session_state.step = 0
            st.rerun()

    with col2:
        if st.button("Next Step", key="next_to_lifestyle"):
            # Save demographic entries to session_state
            st.session_state.fullname = fullname
            st.session_state.birthdate = birthdate
            st.session_state.nationality = nationality
            st.session_state.emailaddress = emailaddress
            st.session_state.currentaddress = currentaddress
            st.session_state.householdcomposition = householdcomposition

            # Attempt to persist demographics to CSV
            try:
                save_path = os.path.join("..", "data", "mock_profiles_demographics.csv")
                row = {
                    "timestamp": datetime.utcnow().isoformat(),
                    "username": st.session_state.username,
                    "fullname": fullname,
                    "birthdate": birthdate,
                    "nationality": nationality,
                    "emailaddress": emailaddress,
                    "currentaddress": currentaddress,
                    "householdcomposition": householdcomposition
                }
                pd.DataFrame([row]).to_csv(save_path, mode="a",
                                           header=not os.path.exists(save_path), index=False)
            except Exception as e:
                st.error(f"Failed to save demographics: {e}")
            else:
                st.session_state.step = 2
                st.rerun()


# --- STEP 2: PRACTICAL REQUIREMENTS ---
elif st.session_state.step == 2:
    st.header("Step 2: Practical Requirements")
    st.write(f"Signed in as: **{st.session_state.username}**")
    st.write(f"These are the requirements you have for your desired community. Please indicate your choices.")
    st.write(f"**Architectural and Physical Space Preferences**")

    # Desired Location
    desired_location = st.text_input(
        "Desired location (city, neighborhood, or region):",
        placeholder="e.g., Germany, Berlin, Kreuzberg",
        key="desired_location"
    )

    # Size of community
    size_of_community_options = ["Small (<10 people)", "Medium (10–40)", "Large (40–100)","Extra-large (>100)"]
    size_of_community = st.multiselect(
        "What type of community size do you prefer? (you may select multiple):",
        options=size_of_community_options,
        default=[],
        key="size_of_community"
    )

    # Regime of sharing
    regime_of_sharing_options = ["Shared extra spaces (gardens, workshops, guest rooms, garage)", "Shared essential spaces (kitchen, laundry, dining rooms)", "Minimal/no shared spaces"]
    regime_of_sharing = st.multiselect(
        "Which regime of sharing do you prefer? (you may select multiple):",
        options=regime_of_sharing_options,
        default=[],
        key="regime_of_sharing"
    )

    # Physical environment
    physical_environment_options = ["Urban / city-centre", "Suburban", "Rural / nature-based","Eco-village style","Architect-designed","Self-built eco-community","Renovated/retrofit buildings"]
    physical_environment = st.multiselect(
        "Which types of physical environment appeal to you? (you may select multiple):",
        options=physical_environment_options,
        default=[],
        key="physical_environment"
    )

    # Private dwelling
    private_dwelling_options = ["Full kitchen", "Kitchenette","Private outdoor space","Full bathroom","Guest room","Other:"]
    private_dwelling = st.multiselect(
        "What features do you require in your private dwelling? (you may select multiple):",
        options=private_dwelling_options,
        default=[],
        key="private_dwelling"
    )

    st.write(f"**Operational Preferences: Daily Governance & Management**")

    # Governance style
    governance_style_options = ["Self-managed (active involvement, working groups)", "Semi-managed (mix of professionals and residents)","Professionally managed","No preference"]
    governance_style = st.multiselect(
        "What governance style do you prefer? (you may select multiple):",
        options=governance_style_options,
        default=[],
        key="governance_style"
    )

    # Cleanliness standard importance
    st.markdown("**How important is each of the following to you?**")

    st.write("Cleanliness standard:")
    st.markdown("""
        <div style="display:flex; justify-content:space-between; font-size:0.85em; color:gray;">
            <span>Not important<br>at all</span>
            <span>Little<br>importance</span>
            <span>Neutral</span>
            <span>Important</span>
            <span>Very<br>important</span>
        </div>
    """, unsafe_allow_html=True)
    cleanliness_importance = st.slider(
        "",
        min_value=1,
        max_value=5,
        value=3,
        key="cleanliness_importance"
    )

    st.write("Quiet hours:")
    st.markdown("""
        <div style="display:flex; justify-content:space-between; font-size:0.85em; color:gray;">
            <span>Not important<br>at all</span>
            <span>Little<br>importance</span>
            <span>Neutral</span>
            <span>Important</span>
            <span>Very<br>important</span>
        </div>
    """, unsafe_allow_html=True)
    quiet_hours_importance = st.slider(
        "",
        min_value=1,
        max_value=5,
        value=3,
        key="quiet_hours_importance"
    )

    st.write("Booking system (for shared spaces):")
    st.markdown("""
        <div style="display:flex; justify-content:space-between; font-size:0.85em; color:gray;">
            <span>Not important<br>at all</span>
            <span>Little<br>importance</span>
            <span>Neutral</span>
            <span>Important</span>
            <span>Very<br>important</span>
        </div>
    """, unsafe_allow_html=True)
    booking_system_importance = st.slider(
        "",
        min_value=1,
        max_value=5,
        value=3,
        key="booking_system_importance"
    )

    st.write("Guest policy:")
    st.markdown("""
        <div style="display:flex; justify-content:space-between; font-size:0.85em; color:gray;">
            <span>Not important<br>at all</span>
            <span>Little<br>importance</span>
            <span>Neutral</span>
            <span>Important</span>
            <span>Very<br>important</span>
        </div>
    """, unsafe_allow_html=True)
    guest_policy_importance = st.slider(
        "",
        min_value=1,
        max_value=5,
        value=3,
        key="guest_policy_importance"
    )

    st.write("Pet policy:")
    st.markdown("""
        <div style="display:flex; justify-content:space-between; font-size:0.85em; color:gray;">
            <span>Not important<br>at all</span>
            <span>Little<br>importance</span>
            <span>Neutral</span>
            <span>Important</span>
            <span>Very<br>important</span>
        </div>
    """, unsafe_allow_html=True)
    pet_policy_importance = st.slider(
        "",
        min_value=1,
        max_value=5,
        value=3,
        key="pet_policy_importance"
    )

    st.write(f"**Institutional Set-Up: Financial & Legal Expectations**")

    # Legal structure
    legal_structure_options = ["Ownership (private unit + share of common areas)", "Cooperative ownership", "Long-term rental","Rental with option to buy","Other:"]
    legal_structure = st.multiselect(
        "What legal structure do you prefer for the community? (you may select multiple):",
        options=legal_structure_options,
        default=[],
        key="legal_structure"
    )

    # Monthly budget
    monthly_budget = st.text_area(
        "Maximum monthly housing budget: (provide range selector)",
        placeholder="Input your budget range here...",
        key="monthly_budget"
    )

    # Other practical requirements
    other_practical_requirements = st.text_area(
        "Other practical requirements (optional):",
        placeholder="Any special requests or preferences...",
        key="other_practical_requirements"
    )

    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back", key="back_to_username_from_practical_requirements"):
            st.session_state.step = 1
            st.rerun()

    with col2:
        if st.button("Next Step", key="next_to_lifestyle"):
            if not desired_location.strip():  # Check if the input is empty or only whitespace
                st.warning("Please enter your desired location before proceeding.")
            else:
                # Save new lifestyle preferences as well
                st.session_state.user_requirements["desired_location"] = desired_location
                st.session_state.user_requirements["size_of_community"] = size_of_community
                st.session_state.user_requirements["regime_of_sharing"] = regime_of_sharing
                st.session_state.user_requirements["physical_environment"] = physical_environment
                st.session_state.user_requirements["private_dwelling"] = private_dwelling

                st.session_state.user_requirements["governance_style"] = governance_style
                st.session_state.user_requirements["cleanliness_importance"] = cleanliness_importance
                st.session_state.user_requirements["quiet_hours_importance"] = quiet_hours_importance
                st.session_state.user_requirements["booking_system_importance"] = booking_system_importance
                st.session_state.user_requirements["guest_policy_importance"] = guest_policy_importance
                st.session_state.user_requirements["pet_policy_importance"] = pet_policy_importance

                st.session_state.user_requirements["legal_structure"] = legal_structure
                st.session_state.user_requirements["monthly_budget"] = monthly_budget

                st.session_state.user_requirements["other_practical_requirements"] = other_practical_requirements
                st.session_state.step = 3  # Proceed to lifestyle preferences step
                st.rerun()


# --- STEP 3: LIFESTYLE PREFERENCES ---
elif st.session_state.step == 3:
    st.header("Step 3: Lifestyle Preferences")
    st.write(f"Signed in as: **{st.session_state.username}**")
    st.write(f"**Relational & Social Interaction Preferences**")

    # Contact with neighbours
    contact_with_neighbours_options = ["Very high", "Moderate", "Low","Only when necessary"]
    contact_with_neighbours = st.multiselect(
        "How much social contact do you prefer with neighbours? (you may select multiple):",
        options=contact_with_neighbours_options,
        default=[],
        key="contact_with_neighbours"
    )

    # Mix of household members
    mix_of_household_options = ["Important", "Neutral", "Not important"]
    mix_of_household = st.multiselect(
        "How important is it for you that the community includes a diverse mix of household types (e.g., singles, couples, families with children, older adults)? (you may select multiple):",
        options=mix_of_household_options,
        default=[],
        key="mix_of_household"
    )

    # Degree of shared responsability
    degree_shared_responsibility_options = ["Strong commitment; active participation", "Moderate involvement", "Occasional participation","Minimal involvement"]
    degree_shared_responsibility = st.multiselect(
        "What degree of shared responsibility do you want? (you may select multiple):",
        options=degree_shared_responsibility_options,
        default=[],
        key="degree_shared_responsibility"
    )

    # Frequency of shared activities
    frequency_shared_activities_options = ["Daily", "Several times a week", "Once a week","Occasionally","Rarely"]
    frequency_shared_activities = st.multiselect(
        "How often would you like shared activities (e.g., shared meals, events)? (you may select multiple):",
        options=frequency_shared_activities_options,
        default=[],
        key="frequency_shared_activities"
    )

    # Communal activities
    communal_activities_options = ["Shared meals", "Gardening", "Childcare", "Cultural/Social events", "Maintenance work"]
    communal_activities = st.multiselect(
        "Which communal activities are important to you? (you may select multiple):",
        options=communal_activities_options,
        default=[],
        key="communal_activities"
    )

    st.write(f"**Lifestyle & Practical Needs**")

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

    # Other Requirements
    other_requirements = st.text_area(
        "Other requirements (optional):",
        placeholder="Any special requests or preferences...",
        key="other_requirements"
    )

    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back", key="back_to_practical_requirements_from_lifestyle"):
            st.session_state.step = 2
            st.rerun()

    with col2:
        if st.button("Next Step", key="next_to_questionnaire"):
            st.session_state.user_requirements["contact_with_neighbours"] = contact_with_neighbours
            st.session_state.user_requirements["mix_of_household"] = mix_of_household
            st.session_state.user_requirements["degree_shared_responsibility"] = degree_shared_responsibility
            st.session_state.user_requirements["frequency_shared_activities"] = frequency_shared_activities
            st.session_state.user_requirements["communal_activities"] = communal_activities

            st.session_state.user_requirements["smoking"] = smoking
            st.session_state.user_requirements["pets"] = pets
            st.session_state.user_requirements["other_requirements"] = other_requirements
            st.session_state.step = 4  # Proceed to personality traits step
            st.rerun()


# --- STEP 4: PERSONALITY TRAITS ---
elif st.session_state.step == 4:
    st.header("Step 4: Personality Traits Questionnaire")
    st.write(f"Signed in as: **{st.session_state.username}**")
    st.write(f"This part of the questionnaire helps map your personality, so that we can match you to the appropriate people. Indicate whether you agree or disagree with the following statements.")

    user_personality_questions = {}
    submit_step1 = False

    for item_num, text in bfi_questions.items():
        st.write(f"**{item_num}. {text}**")

        # Likert labels under slider
        st.markdown("""
            <div style="display:flex; justify-content:space-between; font-size:0.85em; color:gray;">
                <span>Disagree<br>strongly</span>
                <span>Disagree<br>a little</span>
                <span>Neither agree<br>nor disagree</span>
                <span>Agree<br>a little</span>
                <span>Agree<br>strongly</span>
            </div>
        """, unsafe_allow_html=True)

        value = st.slider(
            label="",
            min_value=1,
            max_value=5,
            value=None,
            key=f"bfi_{item_num}"
        )

        user_personality_questions[item_num] = value

        st.markdown("---")


    user_personality = {}

    for trait, items in bfi_scoring.items():
        values = []
        for i in items:
            v = user_personality_questions[i]
            if v is None:
                continue
            if i in reverse_items:
                v = 6 - v  # reverse-scored
            values.append(v)
        user_personality[trait] = sum(values) / len(values)


    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back", key="back_to_lifestyle"):
            st.session_state.step = 3
            st.rerun()

    with col2:
        if st.button("Next Step", key="next_to_description"):
            st.session_state.user_personality = user_personality
            st.session_state.step = 5
            st.rerun()

# --- STEP 5: FREE TEXT DESCRIPTION ---
elif st.session_state.step == 5:
    st.header("Step 5: Tell Us About Your Values")
    st.write(f"Signed in as: **{st.session_state.username}**")
    st.write("Reflect about your values for community living. Please, answer to these questions that make you reflect on how you imagine to live in community. We will infer which values you express most strongly.")

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
        if st.button("← Back", key="back_to_personality_questionnaire"):
            st.session_state.step = 4
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
                # Generate embeddings for the three texts
                texts_to_embed = [living_together, decision_making, personal_contribution]
                # lazy import to avoid expensive work during page load
                from embeddings import get_embeddings
                with st.spinner("Generating semantic embeddings… this may take a few seconds"):
                    embeddings = get_embeddings(texts_to_embed)

                # Save the embeddings for later similarity comparisons
                st.session_state.user_text_embeddings = [arr.tolist() for arr in embeddings]

                # Save + continue if valid
                try:
                    save_path = os.path.join("..", "data", "save_mock_profiles.csv")
                    row = {
                        "timestamp": datetime.utcnow().isoformat(),
                        "username": st.session_state.username,

                        "desired_location": st.session_state.user_requirements.get("desired_location"),
                        "size_of_community": st.session_state.user_requirements.get("size_of_community"),
                        "regime_of_sharing": st.session_state.user_requirements.get("regime_of_sharing"),
                        "physical_environment": st.session_state.user_requirements.get("physical_environment"),
                        "private_dwelling": st.session_state.user_requirements.get("private_dwelling"),
                        "governance_style": st.session_state.user_requirements.get("governance_style"),

                        "cleanliness_importance": st.session_state.user_requirements.get("cleanliness_importance"),
                        "quiet_hours_importance": st.session_state.user_requirements.get("quiet_hours_importance"),
                        "booking_system_importance": st.session_state.user_requirements.get("booking_system_importance"),
                        "guest_policy_importance": st.session_state.user_requirements.get("guest_policy_importance"),
                        "pet_policy_importance": st.session_state.user_requirements.get("pet_policy_importance"),

                        "contact_with_neighbours": st.session_state.user_requirements.get("contact_with_neighbours"),
                        "mix_of_household": st.session_state.user_requirements.get("mix_of_household"),
                        "degree_shared_responsibility": st.session_state.user_requirements.get("degree_shared_responsibility"),
                        "frequency_shared_activities": st.session_state.user_requirements.get("frequency_shared_activities"),
                        "communal_activities": st.session_state.user_requirements.get("communal_activities"),
                        "smoking": st.session_state.user_requirements.get("smoking"),
                        "pets": st.session_state.user_requirements.get("pets"),
                        "other_requirements": st.session_state.user_requirements.get("other_requirements"),

                        "living_together": living_together,
                        "decision_making": decision_making,
                        "personal_contribution": personal_contribution,
                        "living_together_embedding": embeddings[0].tolist(),
                        "decision_making_embedding": embeddings[1].tolist(),
                        "personal_contribution_embedding": embeddings[2].tolist()
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
                st.session_state.step = 6
                st.rerun()

# --- STEP 6: SHOW MATCHES ---
else:
    st.header("Step 6: Your Matches")

    # Load profiles
    profiles_df = pd.read_csv("../data/profiles.csv")

    # -------------------------------
    # APPLY HARD REQUIREMENT FILTERS
    # -------------------------------
    user_req = st.session_state.user_requirements

    # Build a boolean mask to handle multi-select fields
    df = profiles_df.copy()
    mask = pd.Series(True, index=df.index)

    # helper to apply list-or-scalar filtering
    def _apply_pref_mask(field_name, current_mask):
        """Apply preference filter to current_mask and return updated mask."""
        req = user_req.get(field_name, None)
        if not req:
            return current_mask
        if isinstance(req, (list, tuple)):
            if len(req) > 0:
                return current_mask & df[field_name].isin(req)
            return current_mask
        return current_mask & (df[field_name] == req)

    # apply for the multi-select lifestyle fields
    for field in [
        "cleanliness",
        "contact_with_neighbours",
        "mix_of_household",
        "degree_shared_responsibility",
        "frequency_shared_activities",
        "communal_activities"
    ]:
        mask = _apply_pref_mask(field, mask)

    # Apply the remaining exact-match filters (smoking, pets, desired_location)
    mask &= (df["smoking"] == user_req.get("smoking")) & \
            (df["pets"] == user_req.get("pets")) & \
            (df["desired_location"] == user_req.get("desired_location"))

    filtered_df = df[mask]

    # If no profiles match the hard filters:
    if filtered_df.empty:
        st.warning("No matches found that meet all your lifestyle and location requirements.")
        if st.button("Start Over", key="start_over_no_match"):
            st.session_state.step = 0
            st.session_state.user_personality = {}
            st.session_state.user_values = ""
            st.session_state.username = ""
            st.rerun()
        st.stop()

    # -------------------------------
    # CALCULATE PERSONALITY SIMILARITY ON FILTERED PROFILES
    # -------------------------------
    # Calculate value-based similarity

    # Get the personality traits from session state
    user_vector_personality = np.array([float(st.session_state.user_personality[trait]) for trait in bfi_scoring.keys()])

    # Only use the filtered profiles for similarity
    profile_vectors = filtered_df[list(bfi_scoring.keys())].astype(float).values

    personality_similarities = cosine_similarity(user_vector_personality.reshape(1, -1), profile_vectors)[0]

    # -------------------------------
    # EMBEDDINGS SIMILARITY
    # -------------------------------
    # Helper: robust parser for stored embedding cells (list, JSON string, or Python literal)
    def _parse_embedding_cell(val):
        if pd.isna(val):
            return None
        if isinstance(val, (list, tuple, np.ndarray)):
            return np.array(val, dtype=float)
        if isinstance(val, str):
            # try python-literal first
            try:
                parsed = ast.literal_eval(val)
                return np.array(parsed, dtype=float)
            except Exception:
                pass
            # try json
            try:
                parsed = json.loads(val)
                return np.array(parsed, dtype=float)
            except Exception:
                return None
        return None

    # Make sure we have the user's text embeddings saved
    user_text_embeddings = st.session_state.get("user_text_embeddings", None)
    if user_text_embeddings is not None:
        # concat user embeddings into single 1D vector
        try:
            user_vec = np.concatenate([np.array(e, dtype=float).ravel() for e in user_text_embeddings])
        except Exception:
            user_vec = None
    else:
        user_vec = None

    # For each profile in filtered_df, parse its 3 embedding columns and compute cosine similarity
    emb_sims = []
    if user_vec is None:
        emb_sims = [np.nan] * len(filtered_df)
    else:
        for _, row in filtered_df.iterrows():
            e1 = _parse_embedding_cell(row.get("living_together_embedding", None))
            e2 = _parse_embedding_cell(row.get("decision_making_embedding", None))
            e3 = _parse_embedding_cell(row.get("personal_contribution_embedding", None))
            if e1 is None or e2 is None or e3 is None:
                emb_sims.append(np.nan)
                continue
            try:
                profile_vec = np.concatenate([e1.ravel(), e2.ravel(), e3.ravel()])
            except Exception:
                emb_sims.append(np.nan)
                continue
            # dimension check
            if profile_vec.shape != user_vec.shape:
                emb_sims.append(np.nan)
                continue
            sim = float(cosine_similarity(user_vec.reshape(1, -1), profile_vec.reshape(1, -1))[0, 0])
            emb_sims.append(sim)

    # add as a column to the filtered df
    filtered_df = filtered_df.copy()
    filtered_df["personality_similarity"] = personality_similarities
    filtered_df["embeddings_similarity"] = emb_sims

    # Optionally create a combined similarity (uncomment / adjust weights if desired)
    weight_value = 0.5
    weight_embed = 0.5
    filtered_df["combined_similarity"] = filtered_df[["personality_similarity", "embeddings_similarity"]].apply(
        lambda r: (weight_value * r["personality_similarity"] + weight_embed * r["embeddings_similarity"])
        if not pd.isna(r["embeddings_similarity"]) else r["personality_similarity"], axis=1
        )

    # Get top 3 matches
    # choose ranking column for top matches; prefer combined if exists else embeddings_similarity else value similarity
    rank_col = "combined_similarity" if "combined_similarity" in filtered_df.columns else ("embeddings_similarity" if filtered_df["embeddings_similarity"].notna().any() else "personality_similarity")
    top_matches = filtered_df.sort_values(by=rank_col, ascending=False).head(3)

    # -------------------------------
    # DISPLAY RESULTS
    # -------------------------------
    st.write("## 🧩 Your Top 3 Compatibility Matches")
    st.write(f"Showing matches for **{st.session_state.username}**")
    # show both value similarity and embedding similarity if present
    display_cols = ["user_name", "personality_similarity", "embeddings_similarity","combined_similarity"]
    st.dataframe(top_matches[[c for c in display_cols if c in top_matches.columns]])
    # chart combined similarity if available else personality similarity
    chart_col = "combined_similarity" if "combined_similarity" in top_matches.columns and top_matches["combined_similarity"].notna().any() else "personality_similarity"
    st.bar_chart(top_matches.set_index("user_name")[chart_col])

    if st.button("Start Over", key="start_over"):
        st.session_state.step = 0
        st.session_state.user_personality = {}
        st.session_state.user_values = ""
        st.session_state.username = ""
        st.rerun()
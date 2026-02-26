import streamlit as st
import os

def get_demo_mode():
    # 1. URL param
    demo = st.query_params.get("demo")
    if demo:
        return demo.lower()
    return "prod"

def init_session_state():
    demo_mode = get_demo_mode()

    defaults = {
        "step": 0,
        "demo_mode": demo_mode,
        "user_requirements": {},
        "user_personality": {},

        # step 1 - demographics
        "fullname": "",
        "birthdate": "",
        "nationality": "",
        "emailaddress": "",
        "resident_type": "",
        "householdcomposition": "",

        # step 5 – values
        "share_personal_feelings": "",
        "group_disputes": "",
        "group_decision": "",
        "mistake_reaction": None,
        "giving_importance": "",
        "healthy_environments": [],
        "you_creative": "",
        "sharing_unfinished_ideas": None,
        "working_style": None,
    }

    if demo_mode == "sarah":
        defaults.update({
            "fullname": "Sarah Hubert",
            "birthdate": "1990-01-01",
            "nationality": "Germany",
            "emailaddress": "sarah@gmail.com",
            "resident_type": "Joiner: I want to join an existing community",
            "householdcomposition": "With partner",
            "user_requirements": {
                "desired_location": "Sweden, Stockholm",
                "physical_environment": ["Urban / city-centre"],
                "size_of_community": "Small (<10 people)",
                "regime_of_sharing": ["Gardens and outdoor spaces","Guest rooms"],
                "private_dwelling": ["Full kitchen","Full bathroom"],
                "daily_management": ["Contribute to the work"],
                #"cleanliness_importance": 4,
                "quiet_hours_importance": 3,
                #"booking_system_importance": 2,
                "guest_policy_importance": 5,
                #"pet_policy_importance": 4,
                "legal_structure": "Purchase (long-term ownership)",
                "budget_currency": "EUR (€)",
                "available_budget_purchase": 300000,
                "monthly_budget_rent": 0,
                "other_practical_requirements": "Close to public transport and parks.",
                "contact_with_neighbours":2,
                "mix_of_household":3,
                #"degree_shared_responsibility":3,
                "frequency_shared_activities":2,
                "communal_activites":["Shared meals","Childcare"],
                "desired_animals":["cats","dogs"],
                "forbidden_animals":["reptiles"],
                "dietary_restrictions":["Vegetarian"],
                "smoking_tolerance":"Nowhere",
                "hobbies":"Reading, hiking, cooking",
                "other_requirements":"I value sustainability and eco-friendly living."
            },
            "user_personality": {
                "extraversion": 3.5,
                "agreeableness": 4.0,
                "conscientiousness": 4.5,
                "neuroticism": 2.0,
                "openness": 4.8
            },

              # --- Step 5 demo values ---
            "share_personal_feelings": (
                "I like open and honest conversations in a trusted circle, "
                "especially when people listen without judgment."
            ),
            "group_disputes": (
                "I prefer calm dialogue where everyone is heard. "
                "Finding common ground matters more to me than being right."
            ),
            "group_decision": (
                "I would voice my concerns respectfully and try to understand "
                "why the decision was made."
            ),
            "mistake_reaction": (
                "They show compassion and understanding and support me mentally"
            ),
            "giving_importance": (
                "Giving to others is very important to me, especially emotional support "
                "and practical help in everyday life."
            ),
            "healthy_environments": [
                "Humans (Friends, Family and Peers)",
                "Surrounded by nature",
                "Suitable personal living space (nice home)",
                "Infrastructure (school, supermarkets, shopping centre, hospital)",
                "Access to Art & Culture (museum, cinema, concerts)",
            ],
            "you_creative": (
                "Yes, I see myself as creative. I express creativity through cooking, "
                "writing, and finding new ways to solve everyday problems."
            ),
            "sharing_unfinished_ideas": (
                "Comfortable, but I take some time and effort to make my ideas presentable before sharing"
            ),
            "working_style": (
                "I prefer an equal mixture of groupwork and private work. (50/50)"
            ),
        })

    elif demo_mode == "tom":
        defaults.update({
            "fullname": "Tom Müller",
            "birthdate": "1990-01-01",
            "nationality": "Germany",
            "emailaddress": "tom@gmail.com",
            "resident_type": "Joiner: I want to join an existing community",
            "householdcomposition": "With partner",
            "user_requirements": {
                "desired_location": "Sweden, Stockholm",
                "physical_environment": ["Urban / city-centre"],
                "size_of_community": "Small (<10 people)",
                "regime_of_sharing": ["Gardens and outdoor spaces","Guest rooms"],
                "private_dwelling": ["Full kitchen","Full bathroom"],
                "daily_management": ["Contribute to the work"],
                #"cleanliness_importance": 4,
                "quiet_hours_importance": 3,
                #"booking_system_importance": 2,
                "guest_policy_importance": 5,
                #"pet_policy_importance": 4,
                "legal_structure": "Purchase (long-term ownership)",
                "budget_currency": "EUR (€)",
                "available_budget_purchase": 300000,
                "monthly_budget_rent": 0,
                "other_practical_requirements": "Close to public transport and parks.",
                "contact_with_neighbours":2,
                "mix_of_household":3,
                #"degree_shared_responsibility":3,
                "frequency_shared_activities":2,
                "communal_activites":["Shared meals","Childcare"],
                "desired_animals":["cats","dogs"],
                "forbidden_animals":["reptiles"],
                "dietary_restrictions":["Vegetarian"],
                "smoking_tolerance":"Nowhere",
                "hobbies":"Reading, hiking, cooking",
                "other_requirements":"I value sustainability and eco-friendly living."
            },
            "user_personality": {
                "extraversion": 3.5,
                "agreeableness": 4.0,
                "conscientiousness": 4.5,
                "neuroticism": 2.0,
                "openness": 4.8
            },

              # --- Step 5 demo values ---
            "share_personal_feelings": (
                "I like open and honest conversations in a trusted circle, "
                "especially when people listen without judgment."
            ),
            "group_disputes": (
                "I prefer calm dialogue where everyone is heard. "
                "Finding common ground matters more to me than being right."
            ),
            "group_decision": (
                "I would voice my concerns respectfully and try to understand "
                "why the decision was made."
            ),
            "mistake_reaction": (
                "They show compassion and understanding and support me mentally"
            ),
            "giving_importance": (
                "Giving to others is very important to me, especially emotional support "
                "and practical help in everyday life."
            ),
            "healthy_environments": [
                "Humans (Friends, Family and Peers)",
                "Surrounded by nature",
                "Suitable personal living space (nice home)",
                "Infrastructure (school, supermarkets, shopping centre, hospital)",
                "Access to Art & Culture (museum, cinema, concerts)",
            ],
            "you_creative": (
                "Yes, I see myself as creative. I express creativity through cooking, "
                "writing, and finding new ways to solve everyday problems."
            ),
            "sharing_unfinished_ideas": (
                "Comfortable, but I take some time and effort to make my ideas presentable before sharing"
            ),
            "working_style": (
                "I prefer an equal mixture of groupwork and private work. (50/50)"
            ),
        })

    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v
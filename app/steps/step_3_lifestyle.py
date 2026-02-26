import streamlit as st
import csv
import os
import datetime
from data_access.postgres import append_row

from state.navigation import next_step, prev_step
from ui.layout import render_login_info, render_progress_bar


LIFESTYLE_CSV_COLUMNS = [
    "timestamp",
    "username",
    "contact_with_neighbours",
    "mix_of_household",
    "frequency_shared_activities",
    "communal_activities",
    "desired_animals",
    "forbidden_animals",
    "dietary_restrictions",
    "smoking_tolerance",
    "hobbies",
    "other_requirements",
]


def _valid_multiselect_defaults(options: list[str], selected_values) -> list[str]:
    if not isinstance(selected_values, list):
        return []
    return [value for value in selected_values if value in options]


def render():
    render_login_info()
    st.header("Step 3: Lifestyle Preferences")
    col_left, col_video, col_right = st.columns([1, 2, 1])
    with col_video:
        st.video("images/video-placeholder.mp4")

    req = st.session_state.user_requirements

    # -------------------------------------------------
    # Relational & Social Interaction Preferences
    # -------------------------------------------------

    st.subheader("Relational & Social Interaction")

    # Contact with neighbours slider
    st.write("How much social contact do you prefer with neighbours?")
    contact_options = ["Only when necessary", "Low", "Moderate", "Very high"]
    st.markdown(
        """
        <div style="display:flex; justify-content:space-between;
                    font-size:0.85em; color:gray;">
            <span>Only when necessary</span>
            <span>Low</span>
            <span>Moderate</span>
            <span>Very high</span>
        </div>
        """,
        unsafe_allow_html=True
    )
    contact_default = contact_options.index(req.get("contact_with_neighbours")) + 1 if req.get("contact_with_neighbours") in contact_options else 2
    contact_value = st.slider("", 1, 4, contact_default, key="contact_slider")
    req["contact_with_neighbours"] = contact_options[contact_value - 1]

    # Mix of household slider
    st.write("How much importance do you place that there is a diverse mix of household types in your neighborhood? (e.g., individuals, couples, families, seniors, children)")
    mix_options = ["Not important", "Neutral", "Important"]
    st.markdown(
        """
        <div style="display:flex; justify-content:space-between;
                    font-size:0.85em; color:gray;">
            <span>Not important</span>
            <span>Neutral</span>
            <span>Important</span>
        </div>
        """,
        unsafe_allow_html=True
    )
    mix_default = mix_options.index(req.get("mix_of_household")) + 1 if req.get("mix_of_household") in mix_options else 2
    mix_value = st.slider("", 1, 3, mix_default, key="mix_slider")
    req["mix_of_household"] = mix_options[mix_value - 1]

    # Degree shared responsibility slider (Removed in Cycle 14 - Feb 2026)
    #st.write("What is your desired degree of shared responsibility?")
    #degree_options = ["Minimal involvement", "Occasional participation", "Moderate involvement", "Strong commitment; active participation"]
    #st.markdown(
    #    """
    #    <div style="display:flex; justify-content:space-between;
    #                font-size:0.85em; color:gray;">
    #        <span>Minimal involvement</span>
    #        <span>Occasional participation</span>
    #        <span>Moderate involvement</span>
    #        <span>Strong commitment; active participation</span>
    #    </div>
    #    """,
    #    unsafe_allow_html=True
    #)
    #degree_value = st.slider("", 1, 4, 2, key="degree_slider")
    #req["degree_shared_responsibility"] = degree_options[degree_value - 1]

    # Frequency shared activities slider
    st.write("How often would you like to share activities?")
    freq_options = ["Rarely", "Occasionally", "Once a week", "Several times a week", "Daily"]
    st.markdown(
        """
        <div style="display:flex; justify-content:space-between;
                    font-size:0.85em; color:gray;">
            <span>Rarely</span>
            <span>Occasionally</span>
            <span>Once a week</span>
            <span>Several times a week</span>
            <span>Daily</span>
        </div>
        """,
        unsafe_allow_html=True
    )
    freq_default = freq_options.index(req.get("frequency_shared_activities")) + 1 if req.get("frequency_shared_activities") in freq_options else 3
    freq_value = st.slider("", 1, 5, freq_default, key="freq_slider")
    req["frequency_shared_activities"] = freq_options[freq_value - 1]

    req["communal_activities"] = st.multiselect(
        "Which communal activities are important to you? (you may select multiple)",
        options=[
            "Shared meals",
            "Gardening",
            "Childcare",
            "Cultural / Social events",
            "Maintenance work",
            "Other"
        ],
        default=_valid_multiselect_defaults(
            [
                "Shared meals",
                "Gardening",
                "Childcare",
                "Cultural / Social events",
                "Maintenance work",
                "Other"
            ],
            req.get("communal_activities", [])
        ),
    )
    if "Other" in req["communal_activities"]:
        req["communal_activities"] = st.text_input(
            "Please specify your communal activities:",
            value=req.get("communal_activities", "") if "Other" not in req.get("communal_activities") else "",
            placeholder=" "
        )

    # -------------------------------------------------
    # Lifestyle & Practical Needs
    # -------------------------------------------------

    st.subheader("Lifestyle & Practical Needs")

    st.write("Reflect on your preferences for pets.")

    req["desired_animals"] = st.multiselect(
        "What animals would you want to own now or in the future? (you may select multiple)",
        options=["dog", "cat", "rabbit", "hamster", "bird", "fish", "horse", "donkey", "cow", "other"],
        default=_valid_multiselect_defaults(
            ["dog", "cat", "rabbit", "hamster", "bird", "fish", "horse", "donkey", "cow", "other"],
            req.get("desired_animals", [])
        ),
    )
    if "other" in req["desired_animals"]:
        req["desired_animals"] = st.text_input(
            "Please specify your desired animals:",
            value=req.get("desired_animals", "") if "other" not in req.get("desired_animals") else "",
            placeholder=" "
        )

    req["forbidden_animals"] = st.multiselect(
        "What animals would you NOT want to have in your neighborhood? (you may select multiple)",
        options=["dog", "cat", "rabbit", "hamster", "bird", "fish", "horse", "donkey", "cow", "other"],
        default=_valid_multiselect_defaults(
            ["dog", "cat", "rabbit", "hamster", "bird", "fish", "horse", "donkey", "cow", "other"],
            req.get("forbidden_animals", [])
        ),
    )
    if "other" in req["forbidden_animals"]:
        req["forbidden_animals"] = st.text_input(
            "Please specify your forbidden animals:",
            value=req.get("forbidden_animals", "") if "other" not in req.get("forbidden_animals") else "",
            placeholder=" "
        )

    req["dietary_restrictions"] = st.multiselect(
        "What are your dietary restrictions, for shared meals?",
        options=["Vegan","Vegetarian","No restrictions","Other"],
        default=_valid_multiselect_defaults(
            ["Vegan", "Vegetarian", "No restrictions", "Other"],
            req.get("dietary_restrictions", [])
        )
    )
    if "Other" in req["dietary_restrictions"]:
        req["dietary_restrictions"] = st.text_input(
            "Please specify your dietary restrictions:",
            value=req.get("dietary_restrictions", "") if "Other" != req.get("dietary_restrictions") else "",
            placeholder=" "
        )

    req["smoking_tolerance"] = st.multiselect(
        "What is your smoking/vaping tolerance? (you may select multiple)",
        options=[
            "Nowhere",
            "In private spaces",
            "In outdoor spaces",
            "In shared spaces"
        ],
        default=req.get("smoking_tolerance", [])
    )

    req["hobbies"] = st.text_area(
        "What are your hobbies and interests?",
        value=req.get("hobbies", ""),
        placeholder="Write here..."
    )

    req["other_requirements"] = st.text_area(
        "Other requirements (optional):",
        value=req.get("other_requirements", ""),
        placeholder="Any special requests or preferences..."
    )

    # -------------------------------------------------
    # Navigation
    # -------------------------------------------------

    col1, col2 = st.columns([7, 1])

    with col1:
        if st.button("← Back"):
            prev_step()

    with col2:
        if st.button("Next →"):
            # Save answers to CSV
            csv_file_path = os.path.join("..", "data", "saved_answers_lifestyle.csv")
            row = {
                "timestamp": datetime.datetime.utcnow().isoformat(),
                "username": st.session_state.emailaddress,
                "contact_with_neighbours": req.get("contact_with_neighbours", ""),
                "mix_of_household": req.get("mix_of_household", ""),
                "frequency_shared_activities": req.get("frequency_shared_activities", ""),
                "communal_activities": req.get("communal_activities", []),
                "desired_animals": req.get("desired_animals", []),
                "forbidden_animals": req.get("forbidden_animals", []),
                "dietary_restrictions": req.get("dietary_restrictions", []),
                "smoking_tolerance": req.get("smoking_tolerance", []),
                "hobbies": req.get("hobbies", ""),
                "other_requirements": req.get("other_requirements", ""),
            }
            file_exists = os.path.isfile(csv_file_path)
            with open(csv_file_path, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=LIFESTYLE_CSV_COLUMNS, extrasaction="ignore")
                if not file_exists:
                    writer.writeheader()
                writer.writerow(row)

            append_row("saved_answers_lifestyle", row)
            next_step()

    render_progress_bar()
import streamlit as st
import csv
import os
import datetime
from data_access.postgres import append_row

from state.navigation import next_step, prev_step
from ui.layout import render_login_info, render_progress_bar


PRACTICAL_CSV_COLUMNS = [
    "timestamp",
    "username",
    "desired_location",
    "physical_environment",
    "size_of_community",
    "regime_of_sharing",
    "private_dwelling",
    "daily_management",
    "quiet_hours_importance",
    "guest_policy_importance",
    "legal_structure",
    "budget_currency",
    "available_budget_purchase",
    "monthly_budget_rent",
    "other_practical_requirements",
]


def _valid_multiselect_defaults(options: list[str], selected_values) -> list[str]:
    if not isinstance(selected_values, list):
        return []
    return [value for value in selected_values if value in options]


def render():
    render_login_info()

    st.header("Step 2: Practical Requirements")
    st.write("These are the requirements you have for your desired community. Please indicate your choices.")
    col_left, col_video, col_right = st.columns([1, 2, 1])
    with col_video:
        st.video("images/video-placeholder.mp4")

    req = st.session_state.user_requirements

    # -------------------------------------------------
    # Architectural & Physical Space Preferences
    # -------------------------------------------------

    st.subheader("Architectural & Physical Space")

    location_options = [
        "--Select a location--",
        "Sweden, Karlstad",
        "Sweden, Stockholm",
        "Sweden, Gothenburg",
        "Sweden (all)",
        "Denmark, Copenhagen",
        "Denmark, Aarhus",
        "Germany, Stuttgart",
        "Germany, Munich",
        "Germany, Brandenburg",
        "Norway (all)",
        "Norway, Oslo",
        "Switzerland (all)",
        "Switzerland, Zurich",
        "Other regions"
    ]
    saved_location = req.get("desired_location", "")
    if saved_location in location_options:
        location_index = location_options.index(saved_location)
    elif saved_location and saved_location != "--Select a location--":
        location_index = location_options.index("Other regions")
    else:
        location_index = 0

    selected_location = st.selectbox(
        "What is your desired location (country, city or region)?",
        options=location_options,
        index=location_index
    )

    if selected_location == "Other regions":
        req["desired_location"] = st.text_input(
            "Please specify your desired location",
            value=saved_location if saved_location not in ("", "Other regions") else "",
            placeholder="e.g. Spain, Barcelona"
        )
    else:
        req["desired_location"] = selected_location

    req["physical_environment"] = st.multiselect(
        "Where would you prefer your physical environment to be? (you may select multiple)",
        options=[
            "Urban / city-centre",
            "Suburban",
            "Rural / nature-based"
        ],
        default=_valid_multiselect_defaults(
            ["Urban / city-centre", "Suburban", "Rural / nature-based"],
            req.get("physical_environment", [])
        )
    )

    req["size_of_community"] = st.multiselect(
        "What community size do you prefer? (you may select multiple)",
        options=[
            "Small (<10 people)",
            "Medium (10–40)",
            "Large (40–100)"
        ],
        default=_valid_multiselect_defaults(
            ["Small (<10 people)", "Medium (10–40)", "Large (40–100)"],
            req.get("size_of_community", [])
        )
    )

    req["regime_of_sharing"] = st.multiselect(
        "What areas would you share with your neighbours? (you may select multiple)",
        options=[
            "Gardens and outdoor spaces",
            "Workshops and hobby rooms",
            "Guest rooms",
            "Garage and parking",
            "Kitchen and dining areas",
            "Laundry facilities",
            "Living rooms and lounges",
            "Minimal/no shared spaces"
        ],
        default=_valid_multiselect_defaults(
            [
                "Gardens and outdoor spaces",
                "Workshops and hobby rooms",
                "Guest rooms",
                "Garage and parking",
                "Kitchen and dining areas",
                "Laundry facilities",
                "Living rooms and lounges",
                "Minimal/no shared spaces"
            ],
            req.get("regime_of_sharing", [])
        )
    )

    req["private_dwelling"] = st.multiselect(
        "What features would you require in your private home? (you may select multiple)",
        options=[
            "Full kitchen",
            "Kitchenette",
            "Private outdoor space",
            "Full bathroom",
            "Guest room",
            "Other"
        ],
        default=_valid_multiselect_defaults(
            [
                "Full kitchen",
                "Kitchenette",
                "Private outdoor space",
                "Full bathroom",
                "Guest room",
                "Other"
            ],
            req.get("private_dwelling", [])
        )
    )

    # -------------------------------------------------
    # Daily Governance & Management
    # -------------------------------------------------

    st.subheader("Daily Governance & Management")

    # Removed in Cycle 13 (20 January 2026)
    # req["governance_style"] = st.multiselect(
    #    "What governance style would you prefer? (you may select multiple)",
    #   options=[
    #        "Self-managed (active involvement, working groups)",
    #       "Semi-managed (mix of professionals and residents)",
    #        "Professionally managed",
    #        "No preference"
    #    ],
    #    default=req.get("governance_style", [])
    #)

    req["daily_management"] = st.multiselect(
        "Public areas shared among neighbors require work (eg. cleaning, gardening, maintenance). Do you want to be active in managing the community? or would you prefer it being managed for you?",
        options=[
            "Contribute to the work",
            "Work done externally"
        ],
        default=_valid_multiselect_defaults(
            ["Contribute to the work", "Work done externally"],
            req.get("daily_management", [])
        )
    )

    st.markdown("**How important are the following?**")
    #req["cleanliness_importance"] = _importance_slider("Cleanliness standard") # Removed in Cycle 14 (Feb 2026)
    req["quiet_hours_importance"] = _importance_slider(
        "Quiet hours",
        req.get("quiet_hours_importance", 3)
    )
    #req["booking_system_importance"] = _importance_slider("Booking system (shared spaces)") # Removed in Cycle 14 (Feb 2026)
    req["guest_policy_importance"] = _importance_slider(
        "Guest policy",
        req.get("guest_policy_importance", 3)
    )
    #req["pet_policy_importance"] = _importance_slider("Pet policy") # Removed in Cycle 14 (Feb 2026)

    # -------------------------------------------------
    # Financial & Legal Expectations
    # -------------------------------------------------

    st.subheader("Financial & Legal Expectations")

    req["legal_structure"] = st.selectbox(
        "What type of ownership do you prefer?",
        options=[
            "Rental agreement",
            "Purchase (long-term ownership)"
        ],
        index=[
            "Rental agreement",
            "Purchase (long-term ownership)"
        ].index(req.get("legal_structure")) if req.get("legal_structure") in [
            "Rental agreement",
            "Purchase (long-term ownership)"
        ] else None
    )

    st.write("Housing budget for the entire household:")
    col1_budget, col2_budget = st.columns(2)
    with col1_budget:
        req["budget_currency"] = st.selectbox(
            "Currency:",
            options=["EUR (€)", "DKK (kr)", "SEK (kr)"],
            index=["EUR (€)", "DKK (kr)", "SEK (kr)"].index(req.get("budget_currency", "EUR (€)")) if req.get("budget_currency") in ["EUR (€)", "DKK (kr)", "SEK (kr)"] else 0
        )
    with col2_budget:
        if req["legal_structure"] == "Rental agreement":
            req["available_budget_purchase"] = 0
            req["monthly_budget_rent"] = st.number_input(
                "What can you spend on the rent per month?",
                value=req.get("monthly_budget_rent", 0),
                min_value=0,
                step=50
            )
        if req["legal_structure"] == "Purchase (long-term ownership)":
            req["available_budget_purchase"] = st.number_input(
                "What is your available budget for purchase of your home?",
                value=req.get("available_budget_purchase", 0),
                min_value=0,
                step=1000
            )
            req["monthly_budget_rent"] = 0

    req["other_practical_requirements"] = st.text_area(
        "Other practical requirements (optional):",
        value=req.get("other_practical_requirements", "")
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
            if _validate(req):
                # Save answers to CSV
                csv_file_path = os.path.join("..", "data", "saved_answers_practical.csv")
                row = {
                    "timestamp": datetime.datetime.utcnow().isoformat(),
                    "username": st.session_state.emailaddress,
                    "desired_location": req.get("desired_location", ""),
                    "physical_environment": req.get("physical_environment", []),
                    "size_of_community": req.get("size_of_community", []),
                    "regime_of_sharing": req.get("regime_of_sharing", []),
                    "private_dwelling": req.get("private_dwelling", []),
                    "daily_management": req.get("daily_management", []),
                    "quiet_hours_importance": req.get("quiet_hours_importance", 3),
                    "guest_policy_importance": req.get("guest_policy_importance", 3),
                    "legal_structure": req.get("legal_structure", ""),
                    "budget_currency": req.get("budget_currency", "EUR (€)"),
                    "available_budget_purchase": req.get("available_budget_purchase", 0),
                    "monthly_budget_rent": req.get("monthly_budget_rent", 0),
                    "other_practical_requirements": req.get("other_practical_requirements", ""),
                }
                file_exists = os.path.isfile(csv_file_path)
                with open(csv_file_path, mode='a', newline='', encoding='utf-8') as file:
                    writer = csv.DictWriter(file, fieldnames=PRACTICAL_CSV_COLUMNS, extrasaction="ignore")
                    if not file_exists:
                        writer.writeheader()
                    writer.writerow(row)

                append_row("saved_answers_practical", row)
                next_step()

    render_progress_bar()


# -------------------------------------------------
# Helpers
# -------------------------------------------------

def _importance_slider(label: str, default_value: int = 3) -> int:
    st.write(label)
    st.markdown(
        """
        <div style="display:flex; justify-content:space-between;
                    font-size:0.85em; color:gray;">
            <span>Not important</span>
            <span>Very important</span>
        </div>
        """,
        unsafe_allow_html=True
    )
    return st.slider("", 1, 5, int(default_value), key=f"{label}_slider")


def _validate(req: dict) -> bool:
    if not req.get("desired_location", "").strip():
        st.warning("Please enter your desired location before continuing.")
        return False

    return True

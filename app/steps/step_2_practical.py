import streamlit as st

from state.navigation import next_step, prev_step
from ui.layout import render_header


def render():
    render_header()

    st.header("Step 2: Practical Requirements")
    st.write(f"Signed in as: **{st.session_state.username}**")

    req = st.session_state.user_requirements

    # -------------------------------------------------
    # Architectural & Physical Space Preferences
    # -------------------------------------------------

    st.subheader("Architectural & Physical Space Preferences")

    location_options = [
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
    selected_location = st.selectbox(
        "What is your desired location (Country, city or region)?",
        options=location_options
    )

    if selected_location == "Other regions":
        req["desired_location"] = st.text_input(
            "Please specify your desired location",
            value=req.get("desired_location", "") if req.get("desired_location") != "Other regions" else "",
            placeholder="e.g. Spain, Barcelona"
        )
    else:
        req["desired_location"] = selected_location

    req["size_of_community"] = st.multiselect(
        "Preferred community size",
        options=[
            "Small (<10 people)",
            "Medium (10–40)",
            "Large (40–100)",
            "Extra-large (>100)"
        ],
        default=req.get("size_of_community", [])
    )

    req["regime_of_sharing"] = st.multiselect(
        "Preferred regime of sharing",
        options=[
            "Shared extra spaces (gardens, workshops, guest rooms, garage)",
            "Shared essential spaces (kitchen, laundry, dining rooms)",
            "Minimal/no shared spaces"
        ],
        default=req.get("regime_of_sharing", [])
    )

    req["physical_environment"] = st.multiselect(
        "Preferred physical environment",
        options=[
            "Urban / city-centre",
            "Suburban",
            "Rural / nature-based",
            "Eco-village style",
            "Architect-designed",
            "Self-built eco-community",
            "Renovated/retrofit buildings"
        ],
        default=req.get("physical_environment", [])
    )

    req["private_dwelling"] = st.multiselect(
        "Required features in your private dwelling",
        options=[
            "Full kitchen",
            "Kitchenette",
            "Private outdoor space",
            "Full bathroom",
            "Guest room",
            "Other"
        ],
        default=req.get("private_dwelling", [])
    )

    # -------------------------------------------------
    # Operational Preferences
    # -------------------------------------------------

    st.subheader("Operational Preferences: Daily Governance & Management")

    req["governance_style"] = st.multiselect(
        "Preferred governance style",
        options=[
            "Self-managed (active involvement, working groups)",
            "Semi-managed (mix of professionals and residents)",
            "Professionally managed",
            "No preference"
        ],
        default=req.get("governance_style", [])
    )

    st.markdown("**How important are the following?**")

    req["cleanliness_importance"] = _importance_slider("Cleanliness standard")
    req["quiet_hours_importance"] = _importance_slider("Quiet hours")
    req["booking_system_importance"] = _importance_slider("Booking system (shared spaces)")
    req["guest_policy_importance"] = _importance_slider("Guest policy")
    req["pet_policy_importance"] = _importance_slider("Pet policy")

    # -------------------------------------------------
    # Financial & Legal Expectations
    # -------------------------------------------------

    st.subheader("Institutional Set-Up: Financial & Legal Expectations")

    req["legal_structure"] = st.multiselect(
        "Preferred legal structure",
        options=[
            "Ownership (private unit + share of common areas)",
            "Cooperative ownership",
            "Long-term rental",
            "Rental with option to buy",
            "Other"
        ],
        default=req.get("legal_structure", [])
    )

    req["monthly_budget"] = st.text_area(
        "Maximum monthly housing budget",
        value=req.get("monthly_budget", ""),
        placeholder="e.g. €800–€1,200"
    )

    req["other_practical_requirements"] = st.text_area(
        "Other practical requirements (optional)",
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
                next_step()


# -------------------------------------------------
# Helpers
# -------------------------------------------------

def _importance_slider(label: str) -> int:
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
    return st.slider("", 1, 5, 3, key=f"{label}_slider")


def _validate(req: dict) -> bool:
    if not req.get("desired_location", "").strip():
        st.warning("Please enter your desired location before continuing.")
        return False

    return True

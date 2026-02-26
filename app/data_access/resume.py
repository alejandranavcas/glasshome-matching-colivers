import ast
import csv
import datetime
import os
from typing import Any


DATA_DIR = os.path.join("..", "data")

DEMOGRAPHICS_PATH = os.path.join(DATA_DIR, "saved_answers_demographics.csv")
PRACTICAL_PATH = os.path.join(DATA_DIR, "saved_answers_practical.csv")
LIFESTYLE_PATH = os.path.join(DATA_DIR, "saved_answers_lifestyle.csv")
PERSONALITY_PATH = os.path.join(DATA_DIR, "saved_answers_personality.csv")
PERSONALITY_RESPONSES_PATH = os.path.join(DATA_DIR, "saved_answers_personality_responses.csv")
VALUES_PATH = os.path.join(DATA_DIR, "saved_answers_values.csv")


def _normalize_username(username: str) -> str:
    return (username or "").strip().lower()


def _read_rows(path: str) -> list[dict[str, Any]]:
    if not os.path.exists(path):
        return []

    with open(path, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return list(reader)


def _latest_row_for_user(path: str, username: str) -> dict[str, Any] | None:
    target = _normalize_username(username)
    if not target:
        return None

    rows = _read_rows(path)
    if not rows:
        return None

    for row in reversed(rows):
        row_username = _normalize_username(str(row.get("username", "")))
        if row_username == target:
            return row

    return None


def _as_date(value: Any) -> datetime.date | None:
    if value in (None, "", "None"):
        return None

    if isinstance(value, datetime.date):
        return value

    text = str(value).strip()
    try:
        return datetime.date.fromisoformat(text[:10])
    except ValueError:
        return None


def _as_int(value: Any, default: int) -> int:
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return default


def _as_list(value: Any) -> list[str]:
    if value is None:
        return []

    if isinstance(value, list):
        return [str(item) for item in value]

    text = str(value).strip()
    if not text or text in ("None", "nan"):
        return []

    if text.startswith("[") and text.endswith("]"):
        try:
            parsed = ast.literal_eval(text)
            if isinstance(parsed, list):
                return [str(item) for item in parsed]
        except (SyntaxError, ValueError):
            return []

    return [text]


def _build_demographics_state(row: dict[str, Any] | None, username: str) -> dict[str, Any]:
    if not row:
        return {"emailaddress": _normalize_username(username)}

    fullname = row.get("fullname") or row.get("full_name") or ""
    birthdate = row.get("birthdate") or row.get("birth_date")
    emailaddress = (
        row.get("emailaddress")
        or row.get("email_address")
        or row.get("username")
        or username
    )

    householdcomposition = (
        row.get("householdcomposition")
        or row.get("household_composition")
        or row.get("household_compositions")
        or ""
    )

    return {
        "fullname": fullname,
        "birthdate": _as_date(birthdate),
        "nationality": row.get("nationality", ""),
        "emailaddress": _normalize_username(str(emailaddress)),
        "resident_type": row.get("resident_type", ""),
        "householdcomposition": householdcomposition,
    }


def _build_requirements_state(requirements_row: dict[str, Any] | None) -> dict[str, Any]:
    if not requirements_row:
        return {}

    return {
        "desired_location": requirements_row.get("desired_location", ""),
        "physical_environment": _as_list(requirements_row.get("physical_environment")),
        "size_of_community": _as_list(requirements_row.get("size_of_community")),
        "regime_of_sharing": _as_list(requirements_row.get("regime_of_sharing")),
        "private_dwelling": _as_list(requirements_row.get("private_dwelling")),
        "daily_management": _as_list(requirements_row.get("daily_management")),
        "quiet_hours_importance": _as_int(requirements_row.get("quiet_hours_importance"), 3),
        "guest_policy_importance": _as_int(requirements_row.get("guest_policy_importance"), 3),
        "legal_structure": requirements_row.get("legal_structure", ""),
        "budget_currency": requirements_row.get("budget_currency", "EUR (€)"),
        "available_budget_purchase": _as_int(requirements_row.get("available_budget_purchase"), 0),
        "monthly_budget_rent": _as_int(requirements_row.get("monthly_budget_rent"), 0),
        "other_practical_requirements": requirements_row.get("other_practical_requirements", ""),
        "contact_with_neighbours": requirements_row.get("contact_with_neighbours", ""),
        "mix_of_household": requirements_row.get("mix_of_household", ""),
        "frequency_shared_activities": requirements_row.get("frequency_shared_activities", ""),
        "communal_activities": _as_list(
            requirements_row.get("communal_activities")
            or requirements_row.get("communal_activites")
        ),
        "desired_animals": _as_list(requirements_row.get("desired_animals")),
        "forbidden_animals": _as_list(requirements_row.get("forbidden_animals")),
        "dietary_restrictions": _as_list(requirements_row.get("dietary_restrictions")),
        "smoking_tolerance": _as_list(requirements_row.get("smoking_tolerance")),
        "hobbies": requirements_row.get("hobbies", ""),
        "other_requirements": requirements_row.get("other_requirements", ""),
    }


def _build_personality_state(personality_row: dict[str, Any] | None) -> dict[str, Any]:
    if not personality_row:
        return {}

    return {
        "extraversion": float(personality_row.get("extraversion", 0) or 0),
        "agreeableness": float(personality_row.get("agreeableness", 0) or 0),
        "conscientiousness": float(personality_row.get("conscientiousness", 0) or 0),
        "neuroticism": float(personality_row.get("neuroticism", 0) or 0),
        "openness": float(personality_row.get("openness", 0) or 0),
    }


def _build_personality_responses_state(personality_responses_row: dict[str, Any] | None) -> dict[str, int]:
    if not personality_responses_row:
        return {}

    responses: dict[str, int] = {}
    for i in range(1, 45):
        key = f"bfi_{i}"
        if key in personality_responses_row:
            responses[key] = _as_int(personality_responses_row.get(key), 3)

    return responses


def _build_values_state(values_row: dict[str, Any] | None) -> dict[str, Any]:
    if not values_row:
        return {}

    return {
        "share_personal_feelings": values_row.get("share_personal_feelings", ""),
        "group_disputes": values_row.get("group_disputes", ""),
        "group_decision": values_row.get("group_decision", ""),
        "mistake_reaction": values_row.get("mistake_reaction", None),
        "giving_importance": values_row.get("giving_importance", ""),
        "healthy_environments": _as_list(values_row.get("healthy_environments")),
        "you_creative": values_row.get("you_creative", ""),
        "sharing_unfinished_ideas": values_row.get("sharing_unfinished_ideas", None),
        "working_style": values_row.get("working_style", None),
    }


def _compute_resume_step(
    demographics_row: dict[str, Any] | None,
    practical_row: dict[str, Any] | None,
    lifestyle_row: dict[str, Any] | None,
    personality_row: dict[str, Any] | None,
    values_row: dict[str, Any] | None,
) -> int:
    if values_row:
        return 7
    if personality_row:
        return 6
    if lifestyle_row:
        return 5
    if practical_row:
        return 4
    if demographics_row:
        return 3
    return 2


def load_user_progress(username: str) -> dict[str, Any]:
    demographics_row = _latest_row_for_user(DEMOGRAPHICS_PATH, username)
    practical_row = _latest_row_for_user(PRACTICAL_PATH, username)
    lifestyle_row = _latest_row_for_user(LIFESTYLE_PATH, username)
    personality_row = _latest_row_for_user(PERSONALITY_PATH, username)
    personality_responses_row = _latest_row_for_user(PERSONALITY_RESPONSES_PATH, username)
    values_row = _latest_row_for_user(VALUES_PATH, username)

    merged_requirements_row = {}
    if practical_row:
        merged_requirements_row.update(practical_row)
    if lifestyle_row:
        merged_requirements_row.update(lifestyle_row)

    return {
        "demographics": _build_demographics_state(demographics_row, username),
        "requirements": _build_requirements_state(merged_requirements_row or None),
        "personality": _build_personality_state(personality_row),
        "personality_responses": _build_personality_responses_state(personality_responses_row),
        "values": _build_values_state(values_row),
        "resume_step": _compute_resume_step(
            demographics_row,
            practical_row,
            lifestyle_row,
            personality_row,
            values_row,
        ),
    }

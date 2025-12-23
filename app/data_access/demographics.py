import os
import pandas as pd
from datetime import datetime

# -----------------------------
# Configuration
# -----------------------------

DATA_DIR = os.path.join("..", "data")
DEMOGRAPHICS_FILE = "mock_profiles_demographics.csv"

DEMOGRAPHICS_PATH = os.path.join(DATA_DIR, DEMOGRAPHICS_FILE)

DEMOGRAPHICS_COLUMNS = [
    "timestamp",
    "username",
    "fullname",
    "birthdate",
    "nationality",
    "emailaddress",
    "currentaddress",
    "householdcomposition",
]

# -----------------------------
# Internal helpers
# -----------------------------

def _ensure_data_dir():
    os.makedirs(DATA_DIR, exist_ok=True)

def _empty_df():
    return pd.DataFrame(columns=DEMOGRAPHICS_COLUMNS)

def _load_df():
    if not os.path.exists(DEMOGRAPHICS_PATH):
        return _empty_df()
    return pd.read_csv(DEMOGRAPHICS_PATH)

# -----------------------------
# Public API
# -----------------------------

def username_exists(username: str) -> bool:
    """
    Case-insensitive check whether username already exists.
    The considered username is the email address.
    """
    if not username:
        return False

    df = _load_df()
    if df.empty or "username" not in df.columns:
        return False

    return username.strip().lower() in (
        df["username"].astype(str).str.lower().tolist()
    )

def save_demographics_from_state(session_state) -> None:
    """
    Persist demographic fields from st.session_state.
    """
    _ensure_data_dir()

    row = {
        "timestamp": datetime.utcnow().isoformat(),
        "username": session_state.emailaddress,
        "fullname": session_state.fullname,
        "birthdate": session_state.birthdate,
        "nationality": session_state.nationality,
        "emailaddress": session_state.emailaddress,
        "currentaddress": session_state.currentaddress,
        "householdcomposition": session_state.householdcomposition,
    }

    df_new = pd.DataFrame([row])

    if os.path.exists(DEMOGRAPHICS_PATH):
        df_new.to_csv(DEMOGRAPHICS_PATH, mode="a", header=False, index=False)
    else:
        df_new.to_csv(DEMOGRAPHICS_PATH, index=False)

def load_demographics(username: str) -> dict | None:
    """
    Load demographics for a given username.
    Returns a dict or None if not found.
    """
    if not username:
        return None

    df = _load_df()
    if df.empty:
        return None

    row = df[df["username"].astype(str).str.lower() == username.lower()]
    if row.empty:
        return None

    return row.iloc[0].to_dict()

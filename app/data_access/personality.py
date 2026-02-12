import os
import pandas as pd
from datetime import datetime
from data_access.postgres import append_row

# -----------------------------
# Configuration
# -----------------------------

DATA_DIR = os.path.join("..", "data")
PERSONALITY_FILE = "saved_answers_personality.csv"

PERSONALITY_PATH = os.path.join(DATA_DIR, PERSONALITY_FILE)

PERSONALITY_COLUMNS = [
    "timestamp",
    "username",
    "extraversion",
    "agreeableness",
    "conscientiousness",
    "neuroticism",
    "openness",
]

# -----------------------------
# Internal helpers
# -----------------------------

def _ensure_data_dir():
    os.makedirs(DATA_DIR, exist_ok=True)

def _empty_df():
    return pd.DataFrame(columns=PERSONALITY_COLUMNS)

def _load_df():
    if not os.path.exists(PERSONALITY_PATH):
        return _empty_df()
    return pd.read_csv(PERSONALITY_PATH)

# -----------------------------
# Public API
# -----------------------------

def save_personality_from_state(session_state) -> None:
    """
    Persist personality traits from st.session_state.
    """
    _ensure_data_dir()

    row = {
        "timestamp": datetime.utcnow().isoformat(),
        "username": session_state.emailaddress,
        "extraversion": session_state.user_personality.get("extraversion"),
        "agreeableness": session_state.user_personality.get("agreeableness"),
        "conscientiousness": session_state.user_personality.get("conscientiousness"),
        "neuroticism": session_state.user_personality.get("neuroticism"),
        "openness": session_state.user_personality.get("openness"),
    }

    df_new = pd.DataFrame([row])

    if os.path.exists(PERSONALITY_PATH):
        df_new.to_csv(PERSONALITY_PATH, mode="a", header=False, index=False)
    else:
        df_new.to_csv(PERSONALITY_PATH, index=False)

    append_row("saved_answers_personality", row)
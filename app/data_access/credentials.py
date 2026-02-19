from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path

import streamlit_authenticator as stauth


CREDENTIALS_FILE = (
    Path(__file__).resolve().parent.parent.parent
    / "data"
    / "saved_user_credentials.csv"
)
CREDENTIALS_HEADER = [
    "user_id",
    "email",
    "password_hash",
    "created_at",
    "questionnaire_completed",
]


def _ensure_credentials_file() -> None:
    CREDENTIALS_FILE.parent.mkdir(parents=True, exist_ok=True)
    if CREDENTIALS_FILE.exists():
        return

    with CREDENTIALS_FILE.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=CREDENTIALS_HEADER)
        writer.writeheader()


def _normalize_email(email: str) -> str:
    return email.strip().lower()


def _read_rows() -> list[dict[str, str]]:
    _ensure_credentials_file()
    with CREDENTIALS_FILE.open("r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        rows = []
        for row in reader:
            rows.append(
                {
                    "user_id": str(row.get("user_id", "")),
                    "email": str(row.get("email", "")),
                    "password_hash": str(row.get("password_hash", "")),
                    "created_at": str(row.get("created_at", "")),
                    "questionnaire_completed": str(
                        row.get("questionnaire_completed", "False")
                    ),
                }
            )
        return rows


def _write_rows(rows: list[dict[str, str]]) -> None:
    _ensure_credentials_file()
    with CREDENTIALS_FILE.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=CREDENTIALS_HEADER)
        writer.writeheader()
        writer.writerows(rows)


def _hash_password(password: str) -> str:
    return stauth.Hasher.hash(password)


def _check_password(password: str, hashed_password: str) -> bool:
    if not password or not hashed_password:
        return False
    return stauth.Hasher.check_pw(password, hashed_password)


def find_user_by_email(email: str) -> dict[str, str] | None:
    normalized_email = _normalize_email(email)
    for row in _read_rows():
        if _normalize_email(row["email"]) == normalized_email:
            return row
    return None


def create_user(email: str, password: str) -> tuple[bool, str]:
    normalized_email = _normalize_email(email)

    if find_user_by_email(normalized_email):
        return False, "An account with this email already exists."

    rows = _read_rows()
    user_id = str(len(rows) + 1)
    created_at = datetime.now(timezone.utc).isoformat()

    rows.append(
        {
            "user_id": user_id,
            "email": normalized_email,
            "password_hash": _hash_password(password),
            "created_at": created_at,
            "questionnaire_completed": "False",
        }
    )
    _write_rows(rows)
    return True, "Account created successfully."


def authenticate_user(email: str, password: str) -> tuple[bool, str]:
    user = find_user_by_email(email)
    if not user:
        return False, "No account found for this email."

    if not _check_password(password, user["password_hash"]):
        return False, "Incorrect password."

    return True, "Logged in successfully."


def set_questionnaire_completed(email: str) -> None:
    normalized_email = _normalize_email(email)
    rows = _read_rows()
    updated = False

    for row in rows:
        if _normalize_email(row["email"]) == normalized_email:
            row["questionnaire_completed"] = "True"
            updated = True
            break

    if updated:
        _write_rows(rows)

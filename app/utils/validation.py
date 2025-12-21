def min_length(text: str, length: int, label: str) -> str | None:
    if len(text.strip()) < length:
        return f"{label} must be at least {length} characters."
    return None

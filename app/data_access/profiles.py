from utils.embeddings import get_embeddings
from datetime import datetime
import pandas as pd
import os
from data_access.postgres import append_row


def save_texts_with_embeddings(profile: dict):
    texts = [
        profile["share_personal_feelings"],
        profile["group_disputes"],
        profile["group_decision"],
        profile["giving_importance"],
        profile["you_creative"],
    ]

    embeddings = get_embeddings(texts)

    row = {
        "timestamp": datetime.utcnow().isoformat(),
        **profile,
        "share_personal_feelings_embedding": embeddings[0].tolist(),
        "group_disputes_embedding": embeddings[1].tolist(),
        "group_decision_embedding": embeddings[2].tolist(),
        "giving_importance_embedding": embeddings[3].tolist(),
        "you_creative_embedding": embeddings[4].tolist(),
    }

    path = "../data/saved_answers_values.csv"
    pd.DataFrame([row]).to_csv(
        path,
        mode="a",
        header=not os.path.exists(path),
        index=False,
    )

    append_row("saved_answers_values", row)




def save_texts_with_embeddings_2(profile: dict):
    """
    Memory-efficient embedding storage for 512MB instances.
    """
    fields = [
        "share_personal_feelings",
        "group_disputes",
        "group_decision",
        "giving_importance",
        "you_creative",
    ]

    row = {
        "timestamp": datetime.utcnow().isoformat(),
        **profile
    }

    # Process each field individually
    for field in fields:
        text = profile.get(field, "")
        if not text:
            row[f"{field}_embedding"] = []
            continue

        # Generate embedding for one text at a time
        embedding = get_embeddings([text])[0]  # returns a vector

        # Store immediately as list
        row[f"{field}_embedding"] = embedding.tolist()

        # Free memory
        del embedding

    # Save to CSV immediately
    path = "../data/saved_answers_values.csv"
    pd.DataFrame([row]).to_csv(
        path,
        mode="a",
        header=not os.path.exists(path),
        index=False
    )

    append_row("saved_answers_values", row)


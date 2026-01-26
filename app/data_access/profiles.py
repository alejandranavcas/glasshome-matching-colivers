from utils.embeddings import get_embeddings
from datetime import datetime
import pandas as pd
import os


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

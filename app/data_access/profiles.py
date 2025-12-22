from utils.embeddings import get_embeddings
from datetime import datetime
import pandas as pd
import os


def save_profile_with_embeddings(profile: dict):
    texts = [
        profile["living_together"],
        profile["decision_making"],
        profile["personal_contribution"],
    ]

    embeddings = get_embeddings(texts)

    row = {
        "timestamp": datetime.utcnow().isoformat(),
        **profile,
        "living_together_embedding": embeddings[0].tolist(),
        "decision_making_embedding": embeddings[1].tolist(),
        "personal_contribution_embedding": embeddings[2].tolist(),
    }

    path = "../data/save_mock_profiles.csv"
    pd.DataFrame([row]).to_csv(
        path,
        mode="a",
        header=not os.path.exists(path),
        index=False,
    )

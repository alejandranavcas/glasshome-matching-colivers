import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


def find_matches(state):
    df = pd.read_csv("../data/profiles.csv")

    # Apply hard filters
    df = df[df["desired_location"] == state.user_requirements["desired_location"]]

    user_vec = np.array(list(state.user_personality.values())).reshape(1, -1)
    profile_vecs = df[list(state.user_personality.keys())].values

    df["personality_similarity"] = cosine_similarity(user_vec, profile_vecs)[0]

    df = df.sort_values("personality_similarity", ascending=False)
    return df.head(3)

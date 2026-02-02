import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


def find_matches(state):

    # Apply hard filters in lifestyle
    df_lifestyle = pd.read_csv("../data/saved_answers_lifestyle.csv", on_bad_lines='skip') # skip the bad lines due to inconsistent column counts across rows


    requirements_physical_env = state.user_requirements["physical_environment"]
    requirements_size_of_community = state.user_requirements["size_of_community"]
    requirements_regime_of_sharing = state.user_requirements["regime_of_sharing"]
    requirements_private_dwelling = state.user_requirements.get("private_dwelling")

    df = df_lifestyle[
        df_lifestyle["physical_environment"]
            .apply(lambda x: any(env in x for env in requirements_physical_env)) &
        df_lifestyle["size_of_community"]
            .apply(lambda x: any(size in x for size in requirements_size_of_community)) &
        df_lifestyle["regime_of_sharing"]
            .apply(lambda x: any(regime in x for regime in requirements_regime_of_sharing)) &
        df_lifestyle["private_dwelling"]
            .apply(lambda x: any(dwelling in x for dwelling in requirements_private_dwelling))
    ]


    #user_vec = np.array(list(state.user_personality.values())).reshape(1, -1)
    #profile_vecs = df[list(state.user_personality.keys())].values

    #df["personality_similarity"] = cosine_similarity(user_vec, profile_vecs)[0]

    #df = df.sort_values("personality_similarity", ascending=False)
    return df #df.head(3)

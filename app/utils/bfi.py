BFI_QUESTIONS = {
    1: "I am talkative",
    2: "I tend to find fault with others",
    3: "I do a thorough job",
    4: "I am depressed, blue",
    5: "I am original, comes up with new ideas",
    6: "I am reserved",
    7: "I am helpful and unselfish with others",
    8: "I can be somewhat careless",
    9: "I am relaxed, handles stress well",
    10: "I am curious about many different things",
    11: "I am full of energy",
    12: "I start quarrels with others",
    13: "I am a reliable worker",
    14: "I can be tense",
    15: "I am ingenious, a deep thinker",
    16: "I generate a lot of enthusiasm",
    17: "I have a forgiving nature",
    18: "I tend to be disorganized",
    19: "I worry a lot",
    20: "I have an active imagination",
    21: "I tend to be quiet",
    22: "I am generally trusting",
    23: "I tend to be lazy",
    24: "I am emotionally stable, not easily upset",
    25: "I am inventive",
    26: "I have an assertive personality",
    27: "I can be cold and aloof",
    28: "I persevere until the task is finished",
    29: "I can be moody",
    30: "I value artistic, aesthetic experiences",
    31: "I am sometimes shy, inhibited",
    32: "I am considerate and kind to almost everyone",
    33: "I do things efficiently",
    34: "I remain calm in tense situations",
    35: "I prefer work that is routine",
    36: "I am outgoing, sociable",
    37: "I am sometimes rude to others",
    38: "I make plans and follow through with them",
    39: "I get nervous easily",
    40: "I like to reflect, play with ideas",
    41: "I have few artistic interests",
    42: "I like to cooperate with others",
    43: "I am easily distracted",
    44: "I am sophisticated in art, music, or literature"
    }
BFI_SCORING = {
    "extraversion":       [1, 6, 11, 16, 21, 26, 31, 36],
    "agreeableness":      [2, 7, 12, 17, 22, 27, 32, 37, 42],
    "conscientiousness":  [3, 8, 13, 18, 23, 28, 33, 38, 43],
    "neuroticism":        [4, 9, 14, 19, 24, 29, 34, 39],
    "openness":           [5, 10, 15, 20, 25, 30, 35, 40, 41, 44]
}
REVERSE_ITEMS = {2, 6, 8, 9, 12, 18, 21, 23, 24, 27, 31, 34, 35, 37, 41, 43}

def compute_personality(responses: dict):
    traits = {}
    for trait, items in BFI_SCORING.items():
        values = []
        for i in items:
            v = responses.get(i)
            if v is None:
                continue
            if i in REVERSE_ITEMS:
                v = 6 - v
            values.append(v)
        traits[trait] = sum(values) / len(values)
    return traits
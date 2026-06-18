import joblib
import pandas as pd
import numpy as np
import random

# -------------------------
# LOAD MODEL
# -------------------------

model = joblib.load("models/logistic_regression_model.pkl")

# -------------------------
# LOAD DATASET
# -------------------------

df = pd.read_csv("data/ml_dataset.csv")

# -------------------------
# TEAM STATS
# -------------------------

team_stats = df.groupby("TEAM_NAME").mean(numeric_only=True)

# -------------------------
# GET FEATURES
# -------------------------

def get_features(team_a, team_b):

    if team_a not in team_stats.index:
        raise ValueError(f"{team_a} not found in dataset")

    if team_b not in team_stats.index:
        raise ValueError(f"{team_b} not found in dataset")

    a = team_stats.loc[team_a]
    b = team_stats.loc[team_b]

    ortg_diff = a["TEAM_OFF_RATING"] - b["TEAM_OFF_RATING"]
    drtg_diff = a["TEAM_DEF_RATING"] - b["TEAM_DEF_RATING"]
    pace_diff = a["TEAM_PACE"] - b["TEAM_PACE"]

    features = [
        ortg_diff,
        drtg_diff,
        pace_diff
    ]

    # REMOVE NaNs
    features = np.nan_to_num(features)

    return features

# -------------------------
# SINGLE GAME SIMULATION
# -------------------------

def predict_game(team_a, team_b):

    features = get_features(team_a, team_b)

    prob = model.predict_proba([features])[0][1]

    # RANDOMIZED RESULT
    if random.random() < prob:
        return team_a
    else:
        return team_b

# -------------------------
# BEST OF 7 SERIES
# -------------------------

def simulate_series(team_a, team_b):

    wins_a = 0
    wins_b = 0

    while wins_a < 4 and wins_b < 4:

        winner = predict_game(team_a, team_b)

        if winner == team_a:
            wins_a += 1
        else:
            wins_b += 1

    # TEAM A WINS
    if wins_a > wins_b:

        return {
            "winner": team_a,
            "loser": team_b,
            "score": f"4-{wins_b}",
            "summary": f"{team_a} won 4-{wins_b} vs {team_b}"
        }

    # TEAM B WINS
    else:

        return {
            "winner": team_b,
            "loser": team_a,
            "score": f"4-{wins_a}",
            "summary": f"{team_b} won 4-{wins_a} vs {team_a}"
        }

# -------------------------
# SIMULATE ENTIRE ROUND
# -------------------------

def simulate_round(matchups):

    results = []

    for matchup in matchups:

        team_a = matchup[0]
        team_b = matchup[1]

        result = simulate_series(team_a, team_b)

        results.append(result)

    return results

# -------------------------
# PREDICT WINNER
# -------------------------

def predict_winner(team_a, team_b):

    return simulate_series(team_a, team_b)
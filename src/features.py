import pandas as pd

# Load datasets
team_stats = pd.read_csv("../data/all_team_stats.csv")
games = pd.read_csv("../data/playoff_games.csv")

# Keep only important team stats
team_stats = team_stats[
    [
        "TEAM_NAME",
        "OFF_RATING",
        "DEF_RATING",
        "PACE",
        "SEASON"
    ]
]

# Rename columns for clarity
team_stats.columns = [
    "TEAM_NAME",
    "TEAM_OFF_RATING",
    "TEAM_DEF_RATING",
    "TEAM_PACE",
    "SEASON"
]

# Merge team stats into playoff games
merged_df = games.merge(
    team_stats,
    on=["TEAM_NAME", "SEASON"],
    how="left"
)

# Create win/loss target column
merged_df["WON"] = merged_df["WL"].apply(
    lambda x: 1 if x == "W" else 0
)

# Extract opponent abbreviation from MATCHUP column
merged_df["OPP_ABBREVIATION"] = merged_df["MATCHUP"].apply(
    lambda x: x.split()[-1]
)

# Create mapping between abbreviations and full team names
team_mapping = games[["TEAM_ABBREVIATION", "TEAM_NAME"]].drop_duplicates()

team_mapping.columns = [
    "OPP_ABBREVIATION",
    "OPP_TEAM_NAME"
]

# Merge opponent team names
merged_df = merged_df.merge(
    team_mapping,
    on="OPP_ABBREVIATION",
    how="left"
)

# Create opponent stats dataframe
opp_stats = team_stats.copy()

opp_stats.columns = [
    "OPP_TEAM_NAME",
    "OPP_OFF_RATING",
    "OPP_DEF_RATING",
    "OPP_PACE",
    "SEASON"
]

# Merge opponent stats
merged_df = merged_df.merge(
    opp_stats,
    on=["OPP_TEAM_NAME", "SEASON"],
    how="left"
)

# Create feature differences
merged_df["ORTG_DIFF"] = (
    merged_df["TEAM_OFF_RATING"] -
    merged_df["OPP_OFF_RATING"]
)

merged_df["DRTG_DIFF"] = (
    merged_df["TEAM_DEF_RATING"] -
    merged_df["OPP_DEF_RATING"]
)

merged_df["PACE_DIFF"] = (
    merged_df["TEAM_PACE"] -
    merged_df["OPP_PACE"]
)

# Keep final machine learning columns
final_df = merged_df[
    [
        "TEAM_NAME",
        "OPP_TEAM_NAME",
        "SEASON",
        "TEAM_OFF_RATING",
        "TEAM_DEF_RATING",
        "TEAM_PACE",
        "OPP_OFF_RATING",
        "OPP_DEF_RATING",
        "OPP_PACE",
        "ORTG_DIFF",
        "DRTG_DIFF",
        "PACE_DIFF",
        "WON"
    ]
]

# Remove missing values
final_df = final_df.dropna()

# Save ML-ready dataset
final_df.to_csv("../data/ml_dataset.csv", index=False)

print(final_df.head())

print("Machine learning dataset created successfully!")
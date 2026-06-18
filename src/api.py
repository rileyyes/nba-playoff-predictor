from nba_api.stats.endpoints import leaguedashteamstats
import pandas as pd
import time

seasons = [
    '2015-16',
    '2016-17',
    '2017-18',
    '2018-19',
    '2019-20',
    '2020-21',
    '2021-22',
    '2022-23',
    '2023-24',
    '2024-25'
]

all_data = []

for season in seasons:
    print(f"Pulling data for {season}...")

    stats = leaguedashteamstats.LeagueDashTeamStats(
        season=season,
        measure_type_detailed_defense='Advanced'
    )

    df = stats.get_data_frames()[0]

    df["SEASON"] = season

    all_data.append(df)

    time.sleep(1)

final_df = pd.concat(all_data)

print(final_df.head())

final_df.to_csv("../data/all_team_stats.csv", index=False)

print("All seasons saved successfully!")
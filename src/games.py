from nba_api.stats.endpoints import leaguegamelog
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

all_games = []

for season in seasons:
    print(f"Pulling playoff games for {season}...")

    games = leaguegamelog.LeagueGameLog(
        season=season,
        season_type_all_star='Playoffs'
    )

    df = games.get_data_frames()[0]

    df["SEASON"] = season

    all_games.append(df)

    time.sleep(1)

final_games = pd.concat(all_games)

print(final_games.head())

final_games.to_csv("../data/playoff_games.csv", index=False)

print("Playoff games saved successfully!")
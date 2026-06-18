import streamlit as st
from simulator import simulate_round, predict_winner
from streamlit.components.v1 import html

# -------------------------
# PAGE CONFIG
# -------------------------

st.set_page_config(layout="wide")

# -------------------------
# EASTERN CONFERENCE TEAMS
# -------------------------

east_teams = [
    "Boston Celtics",
    "New York Knicks",
    "Milwaukee Bucks",
    "Philadelphia 76ers",
    "Miami Heat",
    "Cleveland Cavaliers",
    "Indiana Pacers",
    "Orlando Magic"
]

# -------------------------
# WESTERN CONFERENCE TEAMS
# -------------------------

west_teams = [
    "Denver Nuggets",
    "Oklahoma City Thunder",
    "Minnesota Timberwolves",
    "Dallas Mavericks",
    "Phoenix Suns",
    "LA Clippers",
    "Golden State Warriors",
    "Los Angeles Lakers"
]

# -------------------------
# TEAM LOGOS
# -------------------------

team_logos = {

    "Boston Celtics": "https://a.espncdn.com/i/teamlogos/nba/500/bos.png",
    "New York Knicks": "https://a.espncdn.com/i/teamlogos/nba/500/ny.png",
    "Milwaukee Bucks": "https://a.espncdn.com/i/teamlogos/nba/500/mil.png",
    "Philadelphia 76ers": "https://a.espncdn.com/i/teamlogos/nba/500/phi.png",
    "Miami Heat": "https://a.espncdn.com/i/teamlogos/nba/500/mia.png",
    "Cleveland Cavaliers": "https://a.espncdn.com/i/teamlogos/nba/500/cle.png",
    "Indiana Pacers": "https://a.espncdn.com/i/teamlogos/nba/500/ind.png",
    "Orlando Magic": "https://a.espncdn.com/i/teamlogos/nba/500/orl.png",

    "Denver Nuggets": "https://a.espncdn.com/i/teamlogos/nba/500/den.png",
    "Oklahoma City Thunder": "https://a.espncdn.com/i/teamlogos/nba/500/okc.png",
    "Minnesota Timberwolves": "https://a.espncdn.com/i/teamlogos/nba/500/min.png",
    "Dallas Mavericks": "https://a.espncdn.com/i/teamlogos/nba/500/dal.png",
    "Phoenix Suns": "https://a.espncdn.com/i/teamlogos/nba/500/phx.png",
    "LA Clippers": "https://a.espncdn.com/i/teamlogos/nba/500/lac.png",
    "Golden State Warriors": "https://a.espncdn.com/i/teamlogos/nba/500/gs.png",
    "Los Angeles Lakers": "https://a.espncdn.com/i/teamlogos/nba/500/lal.png"
}

# -------------------------
# PAGE TITLE
# -------------------------

st.title("🏀 NBA Playoff Bracket Simulator")

st.subheader("Select Playoff Matchups")

east_matchups = []
west_matchups = []

# -------------------------
# EASTERN CONFERENCE
# -------------------------

st.markdown("## Eastern Conference")

for i in range(4):

    col1, col2 = st.columns(2)

    with col1:
        team_a = st.selectbox(
            f"East Match {i+1} Team A",
            east_teams,
            key=f"east_a_{i}"
        )

    with col2:
        team_b = st.selectbox(
            f"East Match {i+1} Team B",
            east_teams,
            key=f"east_b_{i}"
        )

    east_matchups.append((team_a, team_b))

# -------------------------
# WESTERN CONFERENCE
# -------------------------

st.markdown("## Western Conference")

for i in range(4):

    col1, col2 = st.columns(2)

    with col1:
        team_a = st.selectbox(
            f"West Match {i+1} Team A",
            west_teams,
            key=f"west_a_{i}"
        )

    with col2:
        team_b = st.selectbox(
            f"West Match {i+1} Team B",
            west_teams,
            key=f"west_b_{i}"
        )

    west_matchups.append((team_a, team_b))

# -------------------------
# SIMULATE PLAYOFFS
# -------------------------

if st.button("🔥 SIMULATE PLAYOFFS"):

    # ROUND 1
    east_r1 = simulate_round(east_matchups)
    west_r1 = simulate_round(west_matchups)

    # ROUND 2
    east_r2 = simulate_round([
        (east_r1[0]["winner"], east_r1[1]["winner"]),
        (east_r1[2]["winner"], east_r1[3]["winner"])
    ])

    west_r2 = simulate_round([
        (west_r1[0]["winner"], west_r1[1]["winner"]),
        (west_r1[2]["winner"], west_r1[3]["winner"])
    ])

    # CONFERENCE FINALS
    east_champ = predict_winner(
        east_r2[0]["winner"],
        east_r2[1]["winner"]
    )

    west_champ = predict_winner(
        west_r2[0]["winner"],
        west_r2[1]["winner"]
    )

    # NBA FINALS
    nba_champion = predict_winner(
        east_champ["winner"],
        west_champ["winner"]
    )

    # -------------------------
    # MATCHUP CARD FUNCTION
    # -------------------------

    def matchup_card(team):

        return f'''
        <div class="matchup">

            <div class="team-box winner">

                <div class="logo-row">

                    <img class="team-logo"
                         src="{team_logos[team["winner"]]}">

                    <div>

                        <div class="team-name">
                            {team["winner"]}
                        </div>

                        <div class="series-score">
                            def. {team["loser"]} {team["score"]}
                        </div>

                    </div>

                </div>

            </div>

            <div class="connector"></div>

        </div>
        '''

    # -------------------------
    # HTML BRACKET
    # -------------------------

    bracket_html = f"""

    <html>

    <head>

    <style>

    body {{
        background-color: #0e1117;
        color: white;
        font-family: Arial, sans-serif;
        padding: 20px;
    }}

    .bracket-wrapper {{
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 70px;
        overflow-x: auto;
    }}

    .round {{
        display: flex;
        flex-direction: column;
        justify-content: space-around;
        min-height: 950px;
    }}

    .round h3 {{
        text-align: center;
        margin-bottom: 20px;
        color: white;
    }}

    .matchup {{
        position: relative;
        margin: 35px 0;
    }}

    .team-box {{
        background: #1f2937;
        border: 2px solid #374151;
        border-radius: 10px;
        padding: 14px;
        width: 320px;
        margin: 8px 0;
        box-shadow: 0 0 10px rgba(0,0,0,0.4);
    }}

    .winner {{
        border-color: #22c55e;
        background: #14532d;
    }}

    .logo-row {{
        display: flex;
        align-items: center;
        gap: 12px;
    }}

    .team-logo {{
        width: 40px;
        height: 40px;
    }}

    .team-name {{
        font-weight: bold;
        font-size: 15px;
        color: white;
    }}

    .series-score {{
        color: #9ca3af;
        font-size: 11px;
        margin-top: 2px;
        font-weight: 400;
    }}

    .connector {{
        position: absolute;
        right: -70px;
        top: 50%;
        width: 70px;
        height: 2px;
        background: white;
    }}

    .champion-box {{
        background: gold;
        color: black;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        font-size: 24px;
        font-weight: bold;
        margin-top: 40px;
        box-shadow: 0 0 15px rgba(255,215,0,0.8);
    }}

    </style>

    </head>

    <body>

    <div class="bracket-wrapper">

        <!-- EAST ROUND 1 -->
        <div class="round">

            <h3>East Round 1</h3>

            {''.join([
                f'''
                <div class="matchup">

                    <div class="team-box">
                        <div class="logo-row">
                            <img class="team-logo" src="{team_logos[a]}">
                            <span class="team-name">{a}</span>
                        </div>
                    </div>

                    <div class="team-box">
                        <div class="logo-row">
                            <img class="team-logo" src="{team_logos[b]}">
                            <span class="team-name">{b}</span>
                        </div>
                    </div>

                    <div class="connector"></div>

                </div>
                '''
                for a, b in east_matchups
            ])}

        </div>

        <!-- EAST ROUND 2 -->
        <div class="round">

            <h3>East Round 2</h3>

            {''.join([
                matchup_card(team)
                for team in east_r1
            ])}

        </div>

        <!-- EAST FINALS -->
        <div class="round">

            <h3>East Finals</h3>

            {''.join([
                matchup_card(team)
                for team in east_r2
            ])}

        </div>

        <!-- NBA FINALS -->
        <div class="round">

            <h3>NBA Finals</h3>

            {matchup_card(east_champ)}

            {matchup_card(west_champ)}

            <div class="champion-box">
                🏆 {nba_champion["summary"]}
            </div>

        </div>

        <!-- WEST FINALS -->
        <div class="round">

            <h3>West Finals</h3>

            {''.join([
                matchup_card(team)
                for team in west_r2
            ])}

        </div>

        <!-- WEST ROUND 2 -->
        <div class="round">

            <h3>West Round 2</h3>

            {''.join([
                matchup_card(team)
                for team in west_r1
            ])}

        </div>

        <!-- WEST ROUND 1 -->
        <div class="round">

            <h3>West Round 1</h3>

            {''.join([
                f'''
                <div class="matchup">

                    <div class="team-box">
                        <div class="logo-row">
                            <img class="team-logo" src="{team_logos[a]}">
                            <span class="team-name">{a}</span>
                        </div>
                    </div>

                    <div class="team-box">
                        <div class="logo-row">
                            <img class="team-logo" src="{team_logos[b]}">
                            <span class="team-name">{b}</span>
                        </div>
                    </div>

                    <div class="connector"></div>

                </div>
                '''
                for a, b in west_matchups
            ])}

        </div>

    </div>

    </body>
    </html>
    """

    html(bracket_html, height=1600, scrolling=True)
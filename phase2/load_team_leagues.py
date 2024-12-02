from py2neo import Node, Relationship
from env_setup import graph
from utils import load_csv
from tqdm import tqdm  # Importing tqdm for the progress bar

def load_team_leagues(filepath):
    data = load_csv(filepath)
    if not data:
        return

    for row in tqdm(data, desc="Loading Team-League Relationships", unit="relationship"):
        try:
            if not row.get("teamid") or not row.get("leagueid") or not row.get("seasonid"):
                print(f"Invalid row: {row}")
                continue

            team = graph.nodes.match("Team", team_id=int(row["teamid"])).first()
            league = graph.nodes.match("League", league_id=int(row["leagueid"])).first()
            season = graph.nodes.match("Season", season_id=int(row["seasonid"])).first()

            if not team or not league or not season:
                print(f"Missing node for TeamID: {row['teamid']}, LeagueID: {row['leagueid']}, SeasonID: {row['seasonid']}")
                continue

            participates_in = Relationship(team, "PARTICIPATES_IN", league, season_id=int(row["seasonid"]))
            graph.merge(participates_in)

            season_participation = Relationship(team, "PLAYS_IN_SEASON", season)
            graph.merge(season_participation)
        except Exception as e:
            print(f"Error loading team-league relationship for team {row.get('teamid')} and league {row.get('leagueid')}: {e}")
    print("Team-League relationships loaded successfully.")

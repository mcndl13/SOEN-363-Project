from py2neo import Node, Relationship
from env_setup import graph
from utils import load_csv

def load_team_leagues(filepath):
    data = load_csv(filepath)
    if not data:
        return

    for row in data:
        try:
            # Validate required fields
            if not row.get("teamid") or not row.get("leagueid") or not row.get("seasonid"):
                print(f"Invalid row: {row}")
                continue

            # Find the associated team, league, and season
            team = graph.nodes.match("Team", team_id=int(row["teamid"])).first()
            league = graph.nodes.match("League", league_id=int(row["leagueid"])).first()
            season = graph.nodes.match("Season", season_id=int(row["seasonid"])).first()

            if not team:
                print(f"Team not found for TeamID: {row['teamid']}")
                continue
            if not league:
                print(f"League not found for LeagueID: {row['leagueid']}")
                continue
            if not season:
                print(f"Season not found for SeasonID: {row['seasonid']}")
                continue

            # Create Team-League relationship for the given season
            participates_in = Relationship(team, "PARTICIPATES_IN", league, season_id=int(row["seasonid"]))
            graph.merge(participates_in)

            # Connect the team to the specific season
            season_participation = Relationship(team, "PLAYS_IN_SEASON", season)
            graph.merge(season_participation)
        except Exception as e:
            print(f"Error loading team-league relationship for team {row.get('teamid')} and league {row.get('leagueid')}: {e}")
    print("Team-League relationships loaded successfully.")

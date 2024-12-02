from py2neo import Node
from env_setup import graph
from utils import load_csv

def load_teams(filepath):
    data = load_csv(filepath)
    if not data:
        return

    for row in data:
        try:
            team = Node(
                "Team",
                team_id=int(row["teamid"]),
                name=row["teamname"],
                founded_year=int(row["foundedyear"]),
                country=row["country"]
            )
            graph.merge(team, "Team", "team_id")
        except Exception as e:
            print(f"Error loading team {row.get('teamname')}: {e}")
    print("Teams loaded successfully.")


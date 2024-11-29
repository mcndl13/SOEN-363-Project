from py2neo import Node
from env_setup import graph
from utils import load_csv

def load_league(filepath):
    data = load_csv(filepath)
    if not data:
        return

    for row in data:
        try:
            league = Node(
                "League",
                league_id=int(row["leagueid"]),
                name=row["name"],
                country=row["country"]
            )
            graph.merge(league, "League", "league_id")
        except Exception as e:
            print(f"Error loading league {row.get('name')}: {e}")
    print("Leagues loaded successfully.")



from py2neo import Node, Relationship
from env_setup import graph
from utils import load_csv

def load_seasons(filepath):
    data = load_csv(filepath)
    if not data:
        return

    for row in data:
        try:
            league = graph.nodes.match("League", league_id=int(row["leagueid"])).first()
            if league:
                season = Node(
                    "Season",
                    season_id=int(row["seasonid"]),
                    year=int(row["seasonyear"]),
                    start_date=row["startdate"],
                    end_date=row["enddate"]
                )
                graph.merge(season, "Season", "season_id")
                plays_in = Relationship(league, "HAS_SEASON", season)
                graph.merge(plays_in)
        except Exception as e:
            print(f"Error loading season {row.get('seasonid')}: {e}")
    print("Seasons loaded successfully.")


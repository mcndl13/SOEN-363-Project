from py2neo import Node, Relationship
from env_setup import graph
from utils import load_csv
from tqdm import tqdm  # Importing tqdm for the progress bar

def load_matches(filepath):
    data = load_csv(filepath)
    if not data:
        return

    for row in tqdm(data, desc="Loading Matches", unit="match"):
        try:
            home_team = graph.nodes.match("Team", team_id=int(row["hometeamid"])).first()
            away_team = graph.nodes.match("Team", team_id=int(row["awayteamid"])).first()
            season = graph.nodes.match("Season", season_id=int(row["seasonid"])).first()

            if home_team and away_team and season:
                match = Node(
                    "Match",
                    match_id=int(row["matchid"]),
                    date=row["date"],
                    city=row["city"],
                    venue=row["venue"],
                    result=row["result"],
                    winnerteamid=int(row["winnerteamid"]) if row.get("winnerteamid") else None
                )
                graph.merge(match, "Match", "match_id")

                home_rel = Relationship(match, "HOME_TEAM", home_team)
                away_rel = Relationship(match, "AWAY_TEAM", away_team)
                season_rel = Relationship(match, "IN_SEASON", season)

                graph.create(home_rel | away_rel | season_rel)
        except Exception as e:
            print(f"Error loading match {row.get('matchid')}: {e}")
    print("Matches loaded successfully.")

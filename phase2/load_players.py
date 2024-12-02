from py2neo import Node, Relationship
from env_setup import graph
from utils import load_csv

def load_players(filepath):
    data = load_csv(filepath)
    if not data:
        return

    for row in data:
        try:
            # Find the associated team
            team = graph.nodes.match("Team", team_id=int(row["teamid"])).first()

            if team:
                # Create Player node
                player = Node(
                    "Player",
                    player_id=int(row["playerid"]),
                    jersey_number=int(row["jerseynumber"]) if row["jerseynumber"] != "NULL" else None,
                    position=row["position"],
                    first_name=row["firstname"],
                    last_name=row["LastName"],  # Matches typo in table definition
                    age=int(row["age"]) if row["age"] != "NULL" else None,
                    nationality=row["nationality"]
                )
                graph.merge(player, "Player", "player_id")

                # Create relationship between Player and Team
                plays_for = Relationship(player, "PLAYS_FOR", team)
                graph.create(plays_for)
        except Exception as e:
            print(f"Error loading player {row.get('playerid')}: {e}")
    print("Players loaded successfully.")

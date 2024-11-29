from py2neo import Node, Relationship
from env_setup import graph
from utils import load_csv

def load_external_team_mapping(filepath):
    data = load_csv(filepath)
    if not data:
        return

    for row in data:
        try:
            # Ensure `teamid` and `externalapiid` exist and are valid
            if not row.get("teamid") or not row.get("externalapiid"):
                print(f"Invalid row: {row}")
                continue

            team = graph.nodes.match("Team", team_id=int(row["teamid"])).first()
            if team:
                external_mapping = Node("ExternalMapping", api_id=row["externalapiid"])
                graph.merge(external_mapping, "ExternalMapping", "api_id")
                maps_to = Relationship(team, "MAPS_TO", external_mapping)
                graph.create(maps_to)
        except Exception as e:
            print(f"Error loading mapping for team {row.get('teamid')}: {e}")
    print("External team mappings loaded successfully.")

from py2neo import Node, Relationship
from env_setup import graph
from utils import load_csv

def load_match_statistics(filepath):
    data = load_csv(filepath)
    if not data:
        return

    for row in data:
        try:
            # Find the associated match
            match = graph.nodes.match("Match", match_id=int(row["matchid"])).first()

            if match:
                # Create MatchStatistics node
                match_stats = Node(
                    "MatchStatistics",
                    stat_id=int(row["statid"]),
                    possession_home=int(row["possessionhome"]) if row["possessionhome"] != "NULL" else None,
                    possession_away=int(row["possessionaway"]) if row["possessionaway"] != "NULL" else None,
                    shots_on_target_home=int(row["shotsontargethome"]) if row["shotsontargethome"] != "NULL" else None,
                    shots_on_target_away=int(row["shotsontargetaway"]) if row["shotsontargetaway"] != "NULL" else None,
                    shots_off_target_home=int(row["shotsofftargethome"]) if row["shotsofftargethome"] != "NULL" else None,
                    shots_off_target_away=int(row["shotsofftargetaway"]) if row["shotsofftargetaway"] != "NULL" else None,
                    corners_home=int(row["cornershome"]) if row["cornershome"] != "NULL" else None,
                    corners_away=int(row["cornersaway"]) if row["cornersaway"] != "NULL" else None,
                    fouls_home=int(row["foulshome"]) if row["foulshome"] != "NULL" else None,
                    fouls_away=int(row["foulsaway"]) if row["foulsaway"] != "NULL" else None,
                )
                graph.merge(match_stats, "MatchStatistics", "stat_id")

                # Create relationship between Match and MatchStatistics
                has_stats = Relationship(match, "HAS_STATISTICS", match_stats)
                graph.create(has_stats)
        except Exception as e:
            print(f"Error loading match statistics for MatchID {row.get('matchid')}: {e}")
    print("Match statistics loaded successfully.")

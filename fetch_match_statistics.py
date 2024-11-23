import requests
from db_config import get_connection

API_HEADERS = {
    "x-rapidapi-host": "v3.football.api-sports.io",
    "x-rapidapi-key": "XXXXXX"
}

def fetch_and_insert_match_statistics():
    conn = get_connection()
    if conn is None:
        return
    cur = conn.cursor()

    try:
        # Fetch all match IDs, HomeTeamID, and AwayTeamID from the Matches table
        cur.execute("SELECT MatchID, HomeTeamID, AwayTeamID FROM Matches")
        matches = cur.fetchall()

        for match_id, home_team_id, away_team_id in matches:
            url = f"https://v3.football.api-sports.io/fixtures/statistics?fixture={match_id}"
            response = requests.get(url, headers=API_HEADERS)

            if response.status_code != 200:
                print(f"Failed to fetch statistics for MatchID {match_id}. Status: {response.status_code}")
                continue

            stats_data = response.json().get("response", [])
            if not stats_data:
                print(f"No statistics available for MatchID {match_id}")
                continue

            possession_home = possession_away = 0
            shots_on_target_home = shots_on_target_away = 0
            shots_off_target_home = shots_off_target_away = 0
            corners_home = corners_away = 0
            fouls_home = fouls_away = 0
            
            # print(f"\n\nStats for MatchID {match_id}: {stats_data}\n\n")
            

            # Iterate through the statistics for both home and away teams
            for team_stats in stats_data:
                team_id = team_stats["team"]["id"]
                stats = team_stats["statistics"]

                # Get statistics for the home team
                if team_id == home_team_id:
                    possession_home = int(next((stat["value"].replace('%', '') if stat["value"] else 0 for stat in stats if stat["type"] == "Ball Possession"), 0))
                    shots_on_target_home = next((stat["value"] if stat["value"] else 0 for stat in stats if stat["type"] == "Shots on Target"), 0)
                    shots_off_target_home = next((stat["value"] if stat["value"] else 0 for stat in stats if stat["type"] == "Shots off Target"), 0)
                    corners_home = next((stat["value"] if stat["value"] else 0 for stat in stats if stat["type"] == "Corner Kicks"), 0)
                    fouls_home = next((stat["value"] if stat["value"] else 0 for stat in stats if stat["type"] == "Fouls"), 0)

                # Get statistics for the away team
                elif team_id == away_team_id:
                    possession_away = int(next((stat["value"].replace('%', '') if stat["value"] else 0 for stat in stats if stat["type"] == "Ball Possession"), 0))
                    shots_on_target_away = next((stat["value"] if stat["value"] else 0 for stat in stats if stat["type"] == "Shots on Target"), 0)
                    shots_off_target_away = next((stat["value"] if stat["value"] else 0 for stat in stats if stat["type"] == "Shots off Target"), 0)
                    corners_away = next((stat["value"] if stat["value"] else 0 for stat in stats if stat["type"] == "Corner Kicks"), 0)
                    fouls_away = next((stat["value"] if stat["value"] else 0 for stat in stats if stat["type"] == "Fouls"), 0)

            # Insert statistics in MatchStatistics table
            cur.execute("""
                INSERT INTO MatchStatistics (
                    MatchID, PossessionHome, PossessionAway, ShotsOnTargetHome, ShotsOnTargetAway,
                    ShotsOffTargetHome, ShotsOffTargetAway, CornersHome, CornersAway, FoulsHome, FoulsAway
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (MatchID) DO UPDATE SET
                    PossessionHome = EXCLUDED.PossessionHome,
                    PossessionAway = EXCLUDED.PossessionAway,
                    ShotsOnTargetHome = EXCLUDED.ShotsOnTargetHome,
                    ShotsOnTargetAway = EXCLUDED.ShotsOnTargetAway,
                    ShotsOffTargetHome = EXCLUDED.ShotsOffTargetHome,
                    ShotsOffTargetAway = EXCLUDED.ShotsOffTargetAway,
                    CornersHome = EXCLUDED.CornersHome,
                    CornersAway = EXCLUDED.CornersAway,
                    FoulsHome = EXCLUDED.FoulsHome,
                    FoulsAway = EXCLUDED.FoulsAway;
            """, (match_id, possession_home, possession_away, shots_on_target_home, shots_on_target_away,
                  shots_off_target_home, shots_off_target_away, corners_home, corners_away, fouls_home, fouls_away))

        conn.commit()
        print("Match statistics inserted successfully!")
    except Exception as e:
        print(f"Error inserting match statistics: {e}")
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    fetch_and_insert_match_statistics()

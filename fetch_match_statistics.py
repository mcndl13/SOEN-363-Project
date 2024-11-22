import requests  # Library for making HTTP requests
from db_config import get_connection  # Function to establish a database connection

# API headers for authentication and identification
API_HEADERS = {
    "x-rapidapi-host": "v3.football.api-sports.io",  # API host for football data
    "x-rapidapi-key": "XXXXXXX"  # Replace with your valid API key
}

def fetch_and_insert_match_statistics():
    conn = get_connection()
    if conn is None:
        return
    cur = conn.cursor()

    try:
        # Fetch all match IDs from the Matches table
        cur.execute("SELECT MatchID FROM Matches")
        matches = cur.fetchall()

        for (match_id,) in matches:
            # Construct API endpoint for fetching match statistics
            url = f"https://v3.football.api-sports.io/fixtures/statistics?fixture={match_id}"
            response = requests.get(url, headers=API_HEADERS)

            # Check if the API request was successful
            if response.status_code != 200:
                print(f"Failed to fetch statistics for MatchID {match_id}. Status: {response.status_code}")
                continue

            # Parse the response JSON to get the statistics data
            stats_data = response.json().get("response", [])
            if not stats_data:
                print(f"No statistics available for MatchID {match_id}")
                continue

            # Initialize variables for match-level statistics
            possession_home = possession_away = 0
            shots_on_target_home = shots_on_target_away = 0
            shots_off_target_home = shots_off_target_away = 0
            corners_home = corners_away = 0
            fouls_home = fouls_away = 0

            # Iterate through the statistics for both teams (home and away)
            for team_stats in stats_data:
                team_name = team_stats["team"]["name"]  # Get the team name for debugging
                stats = team_stats["statistics"]

                # Log statistics for debugging
                print(f"Processing stats for team: {team_name}")
                print(f"Stats: {stats}")

                # Extract statistics for home and away teams
                if team_name == "Home Team Name Placeholder":  # Replace with actual home team name or ID logic
                    possession_home = int(next((stat["value"].replace('%', '') for stat in stats if stat["type"] == "Ball Possession"), 0))
                    shots_on_target_home = next((stat["value"] for stat in stats if stat["type"] == "Shots on Target"), 0)
                    shots_off_target_home = next((stat["value"] for stat in stats if stat["type"] == "Shots off Target"), 0)
                    corners_home = next((stat["value"] for stat in stats if stat["type"] == "Corner Kicks"), 0)
                    fouls_home = next((stat["value"] for stat in stats if stat["type"] == "Fouls"), 0)
                elif team_name == "Away Team Name Placeholder":  # Replace with actual away team name or ID logic
                    possession_away = int(next((stat["value"].replace('%', '') for stat in stats if stat["type"] == "Ball Possession"), 0))
                    shots_on_target_away = next((stat["value"] for stat in stats if stat["type"] == "Shots on Target"), 0)
                    shots_off_target_away = next((stat["value"] for stat in stats if stat["type"] == "Shots off Target"), 0)
                    corners_away = next((stat["value"] for stat in stats if stat["type"] == "Corner Kicks"), 0)
                    fouls_away = next((stat["value"] for stat in stats if stat["type"] == "Fouls"), 0)

            # Insert or update match-level statistics in MatchStatistics table
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

        # Commit the transaction to save the changes
        conn.commit()
        print("Match statistics inserted successfully!")
    except Exception as e:
        print(f"Error inserting match statistics: {e}")
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    fetch_and_insert_match_statistics()

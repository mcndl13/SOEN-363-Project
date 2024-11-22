import requests
from db_config import get_connection

API_HEADERS = {
    "x-rapidapi-host": "v3.football.api-sports.io",
    "x-rapidapi-key": "your_api_key"  # Replace with your actual API key
}

def fetch_and_insert_match_statistics():
    conn = get_connection()
    if conn is None:
        return
    cur = conn.cursor()

    try:
        # Fetch match IDs for the 2023 season
        cur.execute("SELECT MatchID FROM Matches WHERE SeasonID IN (SELECT SeasonID FROM Seasons WHERE SeasonYear = 2023)")
        matches = cur.fetchall()

        for (match_id,) in matches:
            print(f"Fetching statistics for MatchID: {match_id}")
            url = f"https://v3.football.api-sports.io/fixtures/players?fixture={match_id}"
            response = requests.get(url, headers=API_HEADERS)

            if response.status_code != 200:
                print(f"Failed to fetch statistics for MatchID {match_id}. Status code: {response.status_code}")
                continue

            match_data = response.json().get("response", [])
            for team_data in match_data:
                team_id = team_data["team"]["id"]

                for player_data in team_data["players"]:
                    player = player_data["player"]
                    statistics = player_data["statistics"][0]

                    # Extract PlayerID and MatchID
                    player_id = player["id"]

                    # Check if the player exists in the Players table
                    cur.execute("SELECT COUNT(*) FROM Players WHERE PlayerID = %s", (player_id,))
                    if cur.fetchone()[0] == 0:
                        print(f"Skipping PlayerID {player_id} (not found in Players table).")
                        continue

                    # Extract statistics
                    goals = statistics["goals"].get("total", 0) or 0
                    assists = statistics["goals"].get("assists", 0) or 0
                    yellow_cards = statistics["cards"].get("yellow", 0) or 0
                    red_cards = statistics["cards"].get("red", 0) or 0

                    # Insert into MatchStatistics
                    cur.execute("""
                        INSERT INTO MatchStatistics (PlayerID, MatchID, Goals, Assists, YellowCards, RedCards)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        ON CONFLICT (PlayerID, MatchID) DO NOTHING;
                    """, (player_id, match_id, goals, assists, yellow_cards, red_cards))

        conn.commit()
        print("Match statistics inserted successfully!")
    except Exception as e:
        print(f"Error inserting match statistics: {e}")
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    fetch_and_insert_match_statistics()

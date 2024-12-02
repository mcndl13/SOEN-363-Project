import requests
from db_config import get_connection

API_HEADERS = {
    "x-rapidapi-host": "v3.football.api-sports.io",
    "x-rapidapi-key": "XXXXXX"
}

def populate_defender_stats():
    conn = get_connection()
    if not conn:
        print("Failed to connect to the database.")
        return

    cur = conn.cursor()

    try:
        # Fetch all defenders from the Players table
        cur.execute("SELECT PlayerID FROM Players WHERE Position = 'Defender'")
        defenders = cur.fetchall()

        if not defenders:
            print("No defenders found in the database.")
            return

        # Iterate over each defender
        for (player_id,) in defenders:
            url = f"https://v3.football.api-sports.io/players?id={player_id}&season=2023"
            response = requests.get(url, headers=API_HEADERS)

            if response.status_code != 200:
                print(f"Failed to fetch stats for PlayerID {player_id} (Status: {response.status_code})")
                continue

            # Parse response to get statistics
            stats_data = response.json().get("response", [])
            if not stats_data:
                print(f"No stats available for PlayerID {player_id}.")
                continue

            # Get tackles and interceptions
            stats = stats_data[0]["statistics"][0]["tackles"]
            tackles = stats.get("total", 0)
            interceptions = stats.get("interceptions", 0)

            # Insert defender stats
            cur.execute("""
                INSERT INTO Defender (PlayerID, Tackles, Interceptions)
                VALUES (%s, %s, %s)
                ON CONFLICT (PlayerID) DO NOTHING;
            """, (player_id, tackles, interceptions))

        conn.commit()
        print("Defender statistics successfully inserted.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    populate_defender_stats()

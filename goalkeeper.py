import requests
from db_config import get_connection

API_HEADERS = {
    "x-rapidapi-host": "v3.football.api-sports.io",
    "x-rapidapi-key": "XXXXXX"
}

def populate_goalkeeper_stats():
    conn = get_connection()
    if not conn:
        print("Failed to connect to the database.")
        return

    cur = conn.cursor()

    try:
        # Fetch all goalkeepers from the Players table
        cur.execute("SELECT PlayerID FROM Players WHERE Position = 'Goalkeeper'")
        goalkeepers = cur.fetchall()

        if not goalkeepers:
            print("No goalkeepers found in the database.")
            return

        # Iterate over each goalkeeper
        for (player_id,) in goalkeepers:
            url = f"https://v3.football.api-sports.io/players?id={player_id}&season=2023"
            response = requests.get(url, headers=API_HEADERS)

            if response.status_code != 200:
                print(f"Failed to fetch stats for PlayerID {player_id} (Status: {response.status_code})")
                continue

            stats_data = response.json().get("response", [])
            if not stats_data:
                print(f"No stats available for PlayerID {player_id}.")
                continue

            # Get clean sheets and penalty saves
            stats = stats_data[0]["statistics"][0]
            clean_sheets = stats["goals"].get("conceded", 0)
            penalty_saves = stats["penalty"].get("saved", 0)

            # Insert or skip if stats already exist
            cur.execute("""
                INSERT INTO Goalkeeper (PlayerID, CleanSheets, PenaltySaves)
                VALUES (%s, %s, %s)
                ON CONFLICT (PlayerID) DO NOTHING;
            """, (player_id, clean_sheets, penalty_saves))

        conn.commit()
        print("Goalkeeper statistics successfully inserted.")
    except Exception as e:
        print(f"An error occurred while inserting goalkeeper stats: {e}")
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    populate_goalkeeper_stats()

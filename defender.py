import requests
from db_config import get_connection

API_HEADERS = {
    "x-rapidapi-host": "v3.football.api-sports.io",
    "x-rapidapi-key": "XXXXXXX"  # Replace with your valid API key
}

def populate_defender_stats():
    conn = get_connection()
    if conn is None:
        return
    cur = conn.cursor()

    try:
        # Fetch all defenders from the Players table
        cur.execute("SELECT PlayerID FROM Players WHERE Position = 'Defender'")
        defenders = cur.fetchall()  # Retrieve all rows from the query result

        for (player_id,) in defenders:
            # Construct API endpoint for fetching defender stats
            url = f"https://v3.football.api-sports.io/players?id={player_id}&season=2023"
            response = requests.get(url, headers=API_HEADERS)

            if response.status_code != 200:
                print(f"Failed to fetch stats for PlayerID {player_id}. Status code: {response.status_code}")
                continue

            # Parse the response JSON to get defender stats
            stats_data = response.json().get("response", [])
            if stats_data:
                # Extract relevant statistics
                tackles = stats_data[0]["statistics"][0]["tackles"]["total"]  # Replace with actual API field
                interceptions = stats_data[0]["statistics"][0]["tackles"]["interceptions"]  # Replace with actual API field

                # Insert defender stats into Defender table
                cur.execute("""
                    INSERT INTO Defender (PlayerID, Tackles, Interceptions)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (PlayerID) DO NOTHING;
                """, (player_id, tackles, interceptions))

        # Commit the transaction
        conn.commit()
        print("Defender statistics inserted successfully!")
    except Exception as e:
        print(f"Error inserting defender statistics: {e}")
    finally:
        # Close the database connection
        cur.close()
        conn.close()

if __name__ == "__main__":
    populate_defender_stats()

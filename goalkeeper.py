import requests
from db_config import get_connection

API_HEADERS = {
    "x-rapidapi-host": "v3.football.api-sports.io",
    "x-rapidapi-key": "XXXXXXX"  # Replace with your valid API key
}

def populate_goalkeeper_stats():
    conn = get_connection()
    if conn is None:
        return
    cur = conn.cursor()

    try:
        # Fetch all goalkeepers from the Players table
        cur.execute("SELECT PlayerID FROM Players WHERE Position = 'Goalkeeper'")
        goalkeepers = cur.fetchall()  # Retrieve all rows from the query result

        for (player_id,) in goalkeepers:
            # Construct API endpoint for fetching goalkeeper stats
            url = f"https://v3.football.api-sports.io/players?id={player_id}&season=2023"
            response = requests.get(url, headers=API_HEADERS)

            if response.status_code != 200:
                print(f"Failed to fetch stats for PlayerID {player_id}. Status code: {response.status_code}")
                continue

            # Parse the response JSON to get goalkeeper stats
            stats_data = response.json().get("response", [])
            if stats_data:
                # Extract relevant statistics
                clean_sheets = stats_data[0]["statistics"][0]["goals"]["conceded"]  # Replace with actual API field
                penalty_saves = stats_data[0]["statistics"][0]["penalty"]["saved"]  # Replace with actual API field

                # Insert goalkeeper stats into Goalkeeper table
                cur.execute("""
                    INSERT INTO Goalkeeper (PlayerID, CleanSheets, PenaltySaves)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (PlayerID) DO NOTHING;
                """, (player_id, clean_sheets, penalty_saves))

        # Commit the transaction
        conn.commit()
        print("Goalkeeper statistics inserted successfully!")
    except Exception as e:
        print(f"Error inserting goalkeeper statistics: {e}")
    finally:
        # Close the database connection
        cur.close()
        conn.close()

if __name__ == "__main__":
    populate_goalkeeper_stats()

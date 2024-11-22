import requests
from db_config import get_connection

API_HEADERS = {
    "x-rapidapi-host": "v3.football.api-sports.io",
    "x-rapidapi-key": "XXXXXXX"  # Replace with your actual API key
}

def fetch_and_insert_players():
    # Establish a database connection
    conn = get_connection()
    if conn is None:
        return
    cur = conn.cursor()

    try:
        # Fetch all distinct team IDs for the 2023 season
        cur.execute("""
            SELECT DISTINCT TeamID 
            FROM TeamLeagues 
            WHERE SeasonID IN (
                SELECT SeasonID 
                FROM Seasons 
                WHERE SeasonYear = 2023
            )
        """)
        teams = cur.fetchall()  # Retrieve all rows from the query result

        # Iterate over each team
        for (team_id,) in teams:
            # Construct the API endpoint for fetching players
            url = f"https://v3.football.api-sports.io/players?team={team_id}&season=2023"
            response = requests.get(url, headers=API_HEADERS)

            # Check if the API request was successful
            if response.status_code != 200:
                print(f"Failed to fetch players for TeamID {team_id}. Status code: {response.status_code}")
                continue  # Skip to the next team if the request fails

            # Parse the response JSON to get the list of players
            players = response.json().get("response", [])
            for player_data in players:
                # Extract player details from the API response
                player = player_data["player"]
                player_id = player["id"]
                first_name = player["firstname"]
                last_name = player["lastname"]
                age = player.get("age", None)
                nationality = player["nationality"]
                jersey_number = player_data["statistics"][0]["games"]["number"]  # Jersey number
                position = player_data["statistics"][0]["games"]["position"]  # Player's position

                # Insert player details into the Players table
                cur.execute("""
                    INSERT INTO Players (PlayerID, JerseyNumber, Position, LasttName, FirstName, Age, Nationality, TeamID)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (PlayerID) DO NOTHING;  -- Prevent duplicate entries
                """, (player_id, jersey_number, position, last_name, first_name, age, nationality, team_id))

        # Commit all changes to the database
        conn.commit()
        print("Players inserted successfully!")
    except Exception as e:
        # Handle any exceptions that occur during execution
        print(f"Error inserting players: {e}")
    finally:
        # Ensure resources are released by closing the cursor and connection
        cur.close()
        conn.close()

if __name__ == "__main__":
    fetch_and_insert_players()

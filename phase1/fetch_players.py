import requests
from db_config import get_connection

API_HEADERS = {
    "x-rapidapi-host": "v3.football.api-sports.io",
    "x-rapidapi-key": "XXXXXX"
}

def fetch_and_insert_players():
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
            url = f"https://v3.football.api-sports.io/players?team={team_id}&season=2023"
            response = requests.get(url, headers=API_HEADERS)

            if response.status_code != 200:
                print(f"Failed to fetch players for TeamID {team_id}. Status code: {response.status_code}")
                continue

            players = response.json().get("response", [])
            for player_data in players:
                player = player_data["player"]
                statistics = player_data.get("statistics", [])

                # Extract player details
                player_id = player["id"]
                first_name = player["firstname"]
                last_name = player["lastname"]
                age = player.get("age", None)
                nationality = player["nationality"]

                # Default values for optional fields
                jersey_number = None
                position = None
                if statistics:
                    jersey_number = statistics[0]["games"].get("number", None)
                    position = statistics[0]["games"].get("position", None)

                # Validate age against AgeDomain constraint
                if age is not None and not (0 < age < 100):
                    print(f"Skipping player {player_id} ({first_name} {last_name}) due to invalid age: {age}")
                    continue

                # Insert player details into the Players table
                cur.execute("""
                    INSERT INTO Players (PlayerID, JerseyNumber, Position, LastName, FirstName, Age, Nationality, TeamID)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (PlayerID) DO NOTHING;  -- Prevent duplicate entries
                """, (player_id, jersey_number, position, last_name, first_name, age, nationality, team_id))

        conn.commit()
        print("Players inserted successfully!")
    except Exception as e:
        print(f"Error inserting players: {e}")
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    fetch_and_insert_players()

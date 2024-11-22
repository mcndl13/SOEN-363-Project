import requests
from db_config import get_connection

API_HEADERS = {
    "x-rapidapi-host": "v3.football.api-sports.io",
    "x-rapidapi-key": "your_api_key"
}

def fetch_and_insert_players():
    conn = get_connection()
    if conn is None:
        return
    cur = conn.cursor()

    try:
        # Get all teams for the 2023 season
        cur.execute("SELECT DISTINCT TeamID FROM TeamLeagues WHERE SeasonID IN (SELECT SeasonID FROM Seasons WHERE SeasonYear = 2023)")
        teams = cur.fetchall()

        for (team_id,) in teams:
            url = f"https://v3.football.api-sports.io/players?team={team_id}&season=2023"
            response = requests.get(url, headers=API_HEADERS)

            if response.status_code != 200:
                print(f"Failed to fetch players for TeamID {team_id}. Status code: {response.status_code}")
                continue

            players = response.json().get("response", [])
            for player_data in players:
                player = player_data["player"]
                player_id = player["id"]
                name = player["name"]
                age = player.get("age", None)
                nationality = player["nationality"]

                # Insert player
                cur.execute("""
                    INSERT INTO Players (PlayerID, Name, Age, Nationality, TeamID)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (PlayerID) DO NOTHING;
                """, (player_id, name, age, nationality, team_id))

        conn.commit()
        print("Players inserted successfully!")
    except Exception as e:
        print(f"Error inserting players: {e}")
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    fetch_and_insert_players()

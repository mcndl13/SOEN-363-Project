import requests
from db_config import get_connection

API_HEADERS = {
    "x-rapidapi-host": "free-api-live-football-data.p.rapidapi.com",
    "x-rapidapi-key": "433c6bdd7fmshf10677331de36dap176b31jsn51a9b86bc9ea"
}

def log_query(query):
    # Write the query exactly as it is into the text file
    with open("queries_log.txt", "a") as log_file:
        log_file.write(f"{query}\n")

def fetch_and_insert_players():
    conn = get_connection()
    if conn is None:
        print("Error: Could not establish a database connection.")
        return
    cur = conn.cursor()

    try:
        # Retrieve the list of team IDs from the Teams table
        cur.execute("SELECT TeamID FROM Teams")
        teams = cur.fetchall()

        if not teams:
            print("No teams found in the database.")
            return

        for team in teams:
            team_id = team[0]  # Extract TeamID
            print(f"Processing data for TeamID: {team_id}")

            url = "https://free-api-live-football-data.p.rapidapi.com/football-get-list-player"
            querystring = {"teamid": str(team_id)}

            response = requests.get(url, headers=API_HEADERS, params=querystring)

            if response.status_code != 200:
                print(f"Failed to fetch players for TeamID {team_id}. Status code: {response.status_code}")
                continue

            try:
                data = response.json()
            except Exception as e:
                print(f"Error parsing JSON for TeamID {team_id}: {e}")
                continue

            response_data = data.get("response")
            if not response_data or not isinstance(response_data, dict):
                print(f"Unexpected 'response' format for TeamID {team_id}. Full response: {response_data}")
                continue

            players_data = response_data.get("list", [])
            if not players_data:
                print(f"No player data found for TeamID {team_id}.")
                continue

            for category in players_data:
                members = category.get("members", [])
                for player_data in members:
                    if not isinstance(player_data, dict):
                        continue

                    try:
                        player_id = player_data.get("id")
                        name = player_data.get("name", "")
                        first_name, last_name = name.split(" ", 1) if " " in name else (name, "")
                        age = None  # Age is not provided in the sample response
                        nationality = player_data.get("cname", "")
                        jersey_number = player_data.get("shirtNumber", 0)
                        position = player_data.get("role", {}).get("fallback", "Unknown")

                        if player_id is None:
                            print(f"Missing player_id for player {first_name} {last_name} in TeamID {team_id}")
                            continue

                        # Check the role and insert accordingly
                        role = position.lower() if position else "unknown"

                        # Insert player into Players table
                        insert_player_query = f"""
                            INSERT INTO Players (PlayerID, FirstName, LasttName, JerseyNumber, Nationality, TeamID, Age, Position) 
                            VALUES ({player_id}, '{first_name}', '{last_name}', {jersey_number}, '{nationality}', {team_id}, 1, '{position}');
                        """


                        # Log the query in the required format (just the query)
                        log_query(insert_player_query)

                        cur.execute(insert_player_query)

                        # For Goalkeepers, insert into Goalkeeper table
                        if role == "keeper":
                            insert_goalkeeper_query = f"""
                                INSERT INTO Goalkeeper (PlayerID) 
                                VALUES ({player_id});
                            """
          
                            log_query(insert_goalkeeper_query)
                            cur.execute(insert_goalkeeper_query)

                        # For Defenders, insert into Defender table
                        elif role == "defender":
                            insert_defender_query = f"""
                                INSERT INTO Defender (PlayerID) 
                                VALUES ({player_id});
                            """
             
                            log_query(insert_defender_query)
                            cur.execute(insert_defender_query)

                    except KeyError as e:
                        print(f"Missing key {e} for player {player_data}")
                        continue
                    except Exception as e:
                        print(f"Error inserting player {first_name} {last_name} for TeamID {team_id}: {e}")
                        conn.rollback()  # Rollback transaction for this player if an error occurs
                        continue

        # Commit all changes to the database
        print("Committing transaction to database.")
        conn.commit()

    except Exception as e:
        print(f"Error during operation: {e}")
        conn.rollback()  # Rollback in case of unexpected error
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    fetch_and_insert_players()

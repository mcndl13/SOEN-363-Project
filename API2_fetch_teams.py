import requests
from db_config import get_connection

API_HEADERS = {
    "x-rapidapi-host": "free-api-live-football-data.p.rapidapi.com",
    "x-rapidapi-key": "xxxxxxx"
}

def fetch_and_insert_teams():
    conn = get_connection()
    if conn is None:
        print("Error: Could not establish a database connection.")
        return
    cur = conn.cursor()

    try:
      
        cur.execute("SELECT LeagueID FROM League") 
        leagues = cur.fetchall()
        
        if not leagues:
            print("No leagues found in the database.")
            return
        

        for league in leagues:
            league_id = league[0]  # Extract LeagueID

            print(f"Fetching teams for LeagueID: {league_id}")
            

            url = "https://free-api-live-football-data.p.rapidapi.com/football-get-list-all-team"
            querystring = {"leagueid": str(league_id)}  
            
            response = requests.get(url, headers=API_HEADERS, params=querystring)

            if response.status_code != 200:
                print(f"Failed to fetch teams for LeagueID {league_id}. Status code: {response.status_code}")
                continue

            try:
                data = response.json()
            except Exception as e:
                print(f"Error parsing JSON for LeagueID {league_id}: {e}")
                continue


            response_data = data.get("response")
            if not response_data or not isinstance(response_data, dict):
                print(f"Unexpected 'response' format for LeagueID {league_id}. Full response: {response_data}")
                continue

            teams = response_data.get("list")
            if not teams or not isinstance(teams, list):
                print(f"No teams found for LeagueID {league_id}.")
                continue

            #Insert teams into the Teams table
            for team in teams:
                if not isinstance(team, dict):
                    print(f"Unexpected element in teams for LeagueID {league_id}: {team}")
                    continue
                
                # Extract relevant fields for the Teams table
                team_id = team.get("id")
                team_name = team.get("name", "Unknown")
                founded_year = team.get("foundedYear", None)  # May be None if not provided
                country = team.get("country", None)  # May be None if not provided

                print(f"Inserting Team: {team_name} (ID: {team_id}) for LeagueID {league_id}")

                try:
                    # Insert team data into the Teams table
                    cur.execute("""
                        INSERT INTO Teams (TeamID, TeamName, FoundedYear, Country)
                        VALUES (%s, %s, %s, %s)
                        ON CONFLICT (TeamID) DO NOTHING;
                    """, (team_id, team_name, founded_year, country))
                except Exception as e:
                    print(f"Error executing SQL for team {team_name}: {e}")
                    conn.rollback()  # Rollback the transaction for this team if there's an error
                    continue

        # Commit all changes to the database
        conn.commit()
        print("Team data inserted successfully for all leagues!")
    
    except Exception as e:
        print(f"Error during operation: {e}")
        conn.rollback()  # Rollback in case of any unexpected error
    finally:
        cur.close()
        conn.close()


import requests  # Library to make HTTP requests
from db_config import get_connection  # Custom function to get a database connection

API_HEADERS = {
    "x-rapidapi-host": "v3.football.api-sports.io",
    "x-rapidapi-key": "XXXXXX"
}

def fetch_and_insert_teams():
    
    conn = get_connection()
    if conn is None:
        return
    cur = conn.cursor()

    try:
        # Fetch the leagues and seasons for the year 2023
        cur.execute("SELECT LeagueID, SeasonID FROM Seasons WHERE SeasonYear = 2023")
        seasons = cur.fetchall() 
        
        # Iterate through each league and season
        for league_id, season_id in seasons:
            url = f"https://v3.football.api-sports.io/teams?league={league_id}&season=2023"
            response = requests.get(url, headers=API_HEADERS)  # Make an API request

            if response.status_code != 200:
                print(f"Failed to fetch teams for LeagueID {league_id}. Status: {response.status_code}")
                continue

            # Get the list of teams
            teams = response.json().get("response", [])
            for team_data in teams:

                team = team_data["team"]
                team_id = team["id"]
                team_name = team["name"]
                founded_year = team.get("founded", None)
                country = team["country"]

                # Insert the team data into the Teams table
                cur.execute("""
                    INSERT INTO Teams (TeamID, TeamName, FoundedYear, Country)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (TeamID) DO NOTHING;  -- Avoid duplicate entries
                """, (team_id, team_name, founded_year, country))

                # Insert the team-league relationship into the TeamLeagues table
                cur.execute("""
                    INSERT INTO TeamLeagues (TeamID, LeagueID, SeasonID)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (TeamID, LeagueID, SeasonID) DO NOTHING;  -- Avoid duplicates
                """, (team_id, league_id, season_id))

        conn.commit()
        print("Teams inserted successfully!")
    except Exception as e:
        print(f"Error inserting teams: {e}")
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    fetch_and_insert_teams()

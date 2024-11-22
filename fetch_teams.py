import requests  # Library to make HTTP requests
from db_config import get_connection  # Custom function to get a database connection

# API headers including host and API key
API_HEADERS = {
    "x-rapidapi-host": "v3.football.api-sports.io",  # API host for football data
    "x-rapidapi-key": "XXXXXXX"  # Replace with your valid API key
}

def fetch_and_insert_teams():
    # Establish a database connection
    conn = get_connection()
    if conn is None:  # Exit if connection cannot be established
        return
    cur = conn.cursor()  # Create a cursor to execute SQL commands

    try:
        # Fetch the leagues and seasons for the year 2023 from the database
        cur.execute("SELECT LeagueID, SeasonID FROM Seasons WHERE SeasonYear = 2023")
        seasons = cur.fetchall()  # Get all rows returned by the query

        # Iterate through each league and season retrieved from the database
        for league_id, season_id in seasons:
            # Construct the API endpoint to fetch teams for the given league and season
            url = f"https://v3.football.api-sports.io/teams?league={league_id}&season=2023"
            response = requests.get(url, headers=API_HEADERS)  # Make an API request

            # Check if the API request was successful
            if response.status_code != 200:
                print(f"Failed to fetch teams for LeagueID {league_id}. Status: {response.status_code}")
                continue  # Skip to the next league if the request fails

            # Extract the list of teams from the API response
            teams = response.json().get("response", [])
            for team_data in teams:
                # Extract relevant team information
                team = team_data["team"]
                team_id = team["id"]  # Team ID from the API
                team_name = team["name"]  # Team name
                founded_year = team.get("founded", None)  # Optional: year team was founded
                country = team["country"]  # Country where the team is based

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

        # Commit all changes to the database
        conn.commit()
        print("Teams inserted successfully!")
    except Exception as e:
        # Print an error message if something goes wrong
        print(f"Error inserting teams: {e}")
    finally:
        # Close the cursor and connection to free up resources
        cur.close()
        conn.close()

# Execute the function if the script is run directly
if __name__ == "__main__":
    fetch_and_insert_teams()

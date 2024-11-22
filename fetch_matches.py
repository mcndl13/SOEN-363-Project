import requests  # Library for making HTTP requests
from db_config import get_connection  # Function to establish a database connection

# API headers for authentication and identification
API_HEADERS = {
    "x-rapidapi-host": "v3.football.api-sports.io",  # API host for football data
    "x-rapidapi-key": "XXXXXXX"  # Replace with your valid API key
}

def fetch_and_insert_matches():
    # Establish a connection to the database
    conn = get_connection()
    if conn is None:  # Exit if connection cannot be established
        return
    cur = conn.cursor()  # Create a cursor object to execute SQL queries

    try:
        # Fetch the leagues and seasons for the year 2023 from the database
        cur.execute("SELECT LeagueID, SeasonID FROM Seasons WHERE SeasonYear = 2023")
        seasons = cur.fetchall()  # Retrieve all rows from the query result

        # Iterate over each league and season
        for league_id, season_id in seasons:
            # Construct the API endpoint for fetching matches
            url = f"https://v3.football.api-sports.io/fixtures?league={league_id}&season=2023"
            response = requests.get(url, headers=API_HEADERS)  # Make a GET request to the API

            # Check if the API request was successful
            if response.status_code != 200:
                print(f"Failed to fetch matches for LeagueID {league_id}. Status: {response.status_code}")
                continue  # Skip to the next league if the request fails

            # Parse the response JSON to get the list of matches
            matches = response.json().get("response", [])
            for match_data in matches:
                # Extract match information from the API response
                match_id = match_data["fixture"]["id"]  # Unique match ID
                date = match_data["fixture"]["date"]  # Match date
                home_team_id = match_data["teams"]["home"]["id"]  # ID of the home team
                away_team_id = match_data["teams"]["away"]["id"]  # ID of the away team
                city = match_data["fixture"]["venue"]["city"]  # City where the match is played
                venue = match_data["fixture"]["venue"]["name"]  # Name of the venue

                # Determine the result of the match
                home_winner = match_data["teams"]["home"]["winner"]  # Whether the home team won
                away_winner = match_data["teams"]["away"]["winner"]  # Whether the away team won
                result = "Draw"  # Default result is "Draw"
                if home_winner:
                    result = "Home"  # Home team wins
                elif away_winner:
                    result = "Away"  # Away team wins

                # Insert match details into the Matches table
                cur.execute("""
                    INSERT INTO Matches (MatchID, Date, HomeTeamID, AwayTeamID, SeasonID, Result, City, Venue)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (MatchID) DO NOTHING;  -- Prevent duplicate entries
                """, (match_id, date, home_team_id, away_team_id, season_id, result, city, venue))

        # Commit all changes to the database
        conn.commit()
        print("Matches inserted successfully!")
    except Exception as e:
        # Handle any exceptions that occur during the process
        print(f"Error inserting matches: {e}")
    finally:
        # Ensure resources are released by closing the cursor and connection
        cur.close()
        conn.close()

# Execute the function if the script is run directly
if __name__ == "__main__":
    fetch_and_insert_matches()

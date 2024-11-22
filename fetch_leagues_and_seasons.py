import requests
from db_config import get_connection

# Headers for API requests, including the API host and API key
API_HEADERS = {
    "x-rapidapi-host": "v3.football.api-sports.io",
    "x-rapidapi-key": "XXXXXXX"  # Replace with your actual API key
}

def fetch_and_insert_leagues_and_seasons():
    # Establish a connection to the database
    conn = get_connection()
    if conn is None:  # Exit if the connection cannot be established
        return
    cur = conn.cursor()  # Create a cursor for executing SQL commands

    try:
        # Define the API endpoint for fetching league information
        url = "https://v3.football.api-sports.io/leagues"
        response = requests.get(url, headers=API_HEADERS)  # Make a GET request to the API

        # Check if the API request was successful
        if response.status_code != 200:
            print(f"Failed to fetch leagues. Status code: {response.status_code}")
            return

        # Parse the JSON response to get the list of leagues
        leagues = response.json().get("response", [])
        
        # Iterate over each league in the API response
        for league in leagues:
            league_id = league["league"]["id"]  # Extract the league ID

            # Filter out leagues not in the range [1, 5]
            if league_id < 1 or league_id > 5:
                continue

            # Extract the league name and country name
            name = league["league"]["name"]
            country = league["country"]["name"]

            # Insert league information into the League table
            cur.execute("""
                INSERT INTO League (LeagueID, Name, Country)
                VALUES (%s, %s, %s)
                ON CONFLICT (LeagueID) DO NOTHING;
            """, (league_id, name, country))

            # Iterate over the seasons of the league
            for season in league["seasons"]:
                # Process only the 2023 season
                if season["year"] == 2023:
                    start_date = season["start"]  # Extract season start date
                    end_date = season["end"]    # Extract season end date

                    # Insert season information into the Seasons table
                    cur.execute("""
                        INSERT INTO Seasons (LeagueID, SeasonYear, StartDate, EndDate)
                        VALUES (%s, %s, %s, %s)
                        ON CONFLICT (LeagueID, SeasonYear) DO NOTHING;
                    """, (league_id, 2023, start_date, end_date))

        # Commit the transaction to save changes to the database
        conn.commit()
        print("Filtered leagues and 2023 seasons inserted successfully!")
    except Exception as e:
        # Print an error message if an exception occurs during execution
        print(f"Error inserting leagues and seasons: {e}")
    finally:
        # Close the cursor and database connection to free resources
        cur.close()
        conn.close()

# Execute the function if the script is run directly
if __name__ == "__main__":
    fetch_and_insert_leagues_and_seasons()

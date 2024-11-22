import requests
import psycopg2

# Database connection details
DB_CONFIG = {
    "dbname": "",
    "user": "",
    "password": "",
    "host": "",
    "port": "",
}

# API details
url = "https://free-api-live-football-data.p.rapidapi.com/football-get-all-leagues"
headers = {
    "x-rapidapi-key": "397db05a70msha1c30e10fb13342p107ec9jsn69f97db5281d",
    "x-rapidapi-host": "free-api-live-football-data.p.rapidapi.com",
}

# Function to fetch leagues from the API
def fetch_leagues_from_api():
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            leagues = response.json().get("response", {}).get("leagues", [])
            return leagues
        else:
            print(f"Error fetching leagues: {response.status_code}")
            return []
    except Exception as e:
        print(f"Error: {e}")
        return []

# Function to insert leagues into PostgreSQL
def insert_leagues(leagues):
    conn = None
    cur = None
    try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        # Insert each league into the League table
        for league in leagues:
            league_id = league.get("id")
            name = league.get("name")
            country = league.get("localizedName")  # Adjust if the API provides a better "country" field
            cur.execute("""
                INSERT INTO League (LeagueID, Name, Country)
                VALUES (%s, %s, %s)
                ON CONFLICT (LeagueID) DO NOTHING;  -- Prevent duplicate entries
            """, (league_id, name, country))

        # Commit the transaction
        conn.commit()
        print("Leagues inserted successfully!")
    except Exception as e:
        print(f"Error inserting leagues: {e}")
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

# Main function to fetch and insert leagues
if __name__ == "__main__":
    leagues = fetch_leagues_from_api()
    if leagues:
        insert_leagues(leagues)
    else:
        print("No leagues to insert.")

import requests
from db_config import get_connection

API_HEADERS = {
    "x-rapidapi-host": "v3.football.api-sports.io",
    "x-rapidapi-key": "XXXXXX"
}

def fetch_and_insert_matches():
    conn = get_connection()
    if conn is None:
        return
    cur = conn.cursor()  

    try:
        # Fetch the leagues and seasons for the year 2023
        cur.execute("SELECT LeagueID, SeasonID FROM Seasons WHERE SeasonYear = 2023")
        seasons = cur.fetchall()

        # Iterate over each league and season
        for league_id, season_id in seasons:
            url = f"https://v3.football.api-sports.io/fixtures?league={league_id}&season=2023"
            response = requests.get(url, headers=API_HEADERS)

            if response.status_code != 200:
                print(f"Failed to fetch matches for LeagueID {league_id}. Status: {response.status_code}")
                continue

            matches = response.json().get("response", [])
            for match_data in matches:
                # Get match information from the API response
                match_id = match_data["fixture"]["id"]
                date = match_data["fixture"]["date"]
                home_team_id = match_data["teams"]["home"]["id"]
                away_team_id = match_data["teams"]["away"]["id"]
                city = match_data["fixture"]["venue"]["city"]
                venue = match_data["fixture"]["venue"]["name"]

                home_winner = match_data["teams"]["home"]["winner"]
                away_winner = match_data["teams"]["away"]["winner"]
                result = "Draw"
                if home_winner:
                    result = "Home"  
                elif away_winner:
                    result = "Away"

                # Insert match details into the Matches table
                cur.execute("""
                    INSERT INTO Matches (MatchID, Date, HomeTeamID, AwayTeamID, SeasonID, Result, City, Venue)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (MatchID) DO NOTHING;  -- Prevent duplicate entries
                """, (match_id, date, home_team_id, away_team_id, season_id, result, city, venue))

        conn.commit()
        print("Matches inserted successfully!")
    except Exception as e:
        print(f"Error inserting matches: {e}")
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    fetch_and_insert_matches()

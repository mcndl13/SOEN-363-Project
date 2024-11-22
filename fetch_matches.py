import requests
from db_config import get_connection

API_HEADERS = {
    "x-rapidapi-host": "v3.football.api-sports.io",
    "x-rapidapi-key": "your_api_key"
}

def fetch_and_insert_matches():
    conn = get_connection()
    if conn is None:
        return
    cur = conn.cursor()

    try:
        cur.execute("SELECT LeagueID, SeasonID FROM Seasons WHERE SeasonYear = 2023")
        seasons = cur.fetchall()

        for league_id, season_id in seasons:
            url = f"https://v3.football.api-sports.io/fixtures?league={league_id}&season=2023"
            response = requests.get(url, headers=API_HEADERS)

            if response.status_code != 200:
                print(f"Failed to fetch matches for LeagueID {league_id}. Status: {response.status_code}")
                continue

            matches = response.json().get("response", [])
            for match_data in matches:
                match_id = match_data["fixture"]["id"]
                date = match_data["fixture"]["date"]
                home_team_id = match_data["teams"]["home"]["id"]
                away_team_id = match_data["teams"]["away"]["id"]
                result = match_data["fixture"]["status"]["short"]

                cur.execute("""
                    INSERT INTO Matches (MatchID, Date, HomeTeamID, AwayTeamID, SeasonID, Result)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT (MatchID) DO NOTHING;
                """, (match_id, date, home_team_id, away_team_id, season_id, result))

        conn.commit()
        print("Matches inserted successfully!")
    except Exception as e:
        print(f"Error inserting matches: {e}")
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    fetch_and_insert_matches()

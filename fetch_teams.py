import requests
from db_config import get_connection

API_HEADERS = {
    "x-rapidapi-host": "v3.football.api-sports.io",
    "x-rapidapi-key": "your_api_key"
}

def fetch_and_insert_teams():
    conn = get_connection()
    if conn is None:
        return
    cur = conn.cursor()

    try:
        cur.execute("SELECT LeagueID, SeasonID FROM Seasons WHERE SeasonYear = 2023")
        seasons = cur.fetchall()

        for league_id, season_id in seasons:
            url = f"https://v3.football.api-sports.io/teams?league={league_id}&season=2023"
            response = requests.get(url, headers=API_HEADERS)

            if response.status_code != 200:
                print(f"Failed to fetch teams for LeagueID {league_id}. Status: {response.status_code}")
                continue

            teams = response.json().get("response", [])
            for team_data in teams:
                team = team_data["team"]
                team_id = team["id"]
                team_name = team["name"]
                founded_year = team.get("founded", None)
                country = team["country"]

                cur.execute("""
                    INSERT INTO Teams (TeamID, TeamName, FoundedYear, Country)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (TeamID) DO NOTHING;
                """, (team_id, team_name, founded_year, country))

                cur.execute("""
                    INSERT INTO TeamLeagues (TeamID, LeagueID, SeasonID)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (TeamID, LeagueID, SeasonID) DO NOTHING;
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

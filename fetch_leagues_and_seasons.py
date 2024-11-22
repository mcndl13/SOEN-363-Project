import requests
from db_config import get_connection

API_HEADERS = {
    "x-rapidapi-host": "v3.football.api-sports.io",
    "x-rapidapi-key": "your_api_key"
}

def fetch_and_insert_leagues_and_seasons():
    conn = get_connection()
    if conn is None:
        return
    cur = conn.cursor()

    try:
        url = "https://v3.football.api-sports.io/leagues"
        response = requests.get(url, headers=API_HEADERS)

        if response.status_code != 200:
            print(f"Failed to fetch leagues. Status code: {response.status_code}")
            return

        leagues = response.json().get("response", [])
        for league in leagues:
            league_id = league["league"]["id"]

            # Filter leagues with ID between 1 and 100
            if league_id < 1 or league_id > 5:
                continue

            name = league["league"]["name"]
            country = league["country"]["name"]

            cur.execute("""
                INSERT INTO League (LeagueID, Name, Country)
                VALUES (%s, %s, %s)
                ON CONFLICT (LeagueID) DO NOTHING;
            """, (league_id, name, country))

            for season in league["seasons"]:
                if season["year"] == 2023:
                    start_date = season["start"]
                    end_date = season["end"]

                    cur.execute("""
                        INSERT INTO Seasons (LeagueID, SeasonYear, StartDate, EndDate)
                        VALUES (%s, %s, %s, %s)
                        ON CONFLICT (LeagueID, SeasonYear) DO NOTHING;
                    """, (league_id, 2023, start_date, end_date))

        conn.commit()
        print("Filtered leagues and 2023 seasons inserted successfully!")
    except Exception as e:
        print(f"Error inserting leagues and seasons: {e}")
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    fetch_and_insert_leagues_and_seasons()

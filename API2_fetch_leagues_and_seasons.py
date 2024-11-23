import requests
from db_config import get_connection

API_HEADERS = {
    "x-rapidapi-host": "free-api-live-football-data.p.rapidapi.com",
    "x-rapidapi-key": "433c6bdd7fmshf10677331de36dap176b31jsn51a9b86bc9ea"
}

def fetch_and_insert_leagues_and_seasons():
    conn = get_connection()
    if conn is None:
        print("Error: Could not establish a database connection.")
        return
    cur = conn.cursor()

    try:
        # Fetch leagues and countries
        url = "https://free-api-live-football-data.p.rapidapi.com/football-get-all-leagues-with-countries"
        response = requests.get(url, headers=API_HEADERS)

        if response.status_code != 200:
            print(f"Failed to fetch countries. Status code: {response.status_code}")
            return

        try:
            data = response.json()
        except Exception as e:
            print(f"Error parsing JSON: {e}")
            return

        # Access the 'response' and 'leagues' keys
        response_data = data.get("response")
        if not response_data or not isinstance(response_data, dict):
            print("Unexpected 'response' format. Full response data:", response_data)
            return

        countries = response_data.get("leagues")
        if not countries or not isinstance(countries, list):
            print("Unexpected 'leagues' format under 'response'.")
            print(f"Value of 'leagues': {countries}")
            return

        for country in countries:
            if not isinstance(country, dict):
                print(f"Unexpected element in countries: {country}")
                continue

            country_name = country.get("name", "Unknown")

            for league in country.get("leagues", []):
                league_id = league.get("id")
                league_name = league.get("name")
                localized_name = league.get("localizedName", "N/A")

                print(f"Inserting League: {league_name}, Country: {country_name}")

                try:
                    cur.execute("""
                        INSERT INTO League (LeagueID, Name, Country)
                        VALUES (%s, %s, %s)
                        ON CONFLICT (LeagueID) DO NOTHING;
                    """, (league_id, league_name, country_name))
                except Exception as e:
                    print(f"Error executing SQL for league {league_name}: {e}")
                    conn.rollback()  # Rollback the transaction
                    continue

                
                season_year = "2024"
                start_date = "2024-08-01"
                end_date = "2025-05-31" 

                print(f"Inserting Season: {season_year} for LeagueID: {league_id}")

                try:
                    cur.execute("""
                        INSERT INTO Seasons (LeagueID, SeasonYear, StartDate, EndDate)
                        VALUES (%s, %s, %s, %s)
                        ON CONFLICT (LeagueID, SeasonYear) DO NOTHING;
                    """, (league_id, season_year, start_date, end_date))
                except Exception as e:
                    print(f"Error executing SQL for season {season_year}: {e}")
                    conn.rollback()  # Rollback the transaction
                    continue

        conn.commit()
        print("Leagues and season data inserted successfully!")
    except Exception as e:
        print(f"Error during operation: {e}")
        conn.rollback()  # Rollback the transaction in case of any other error
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    fetch_and_insert_leagues_and_seasons()
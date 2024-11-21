from api import fetch_league_data, fetch_season_data, fetch_country_data

def main():
    # Fetching data
    fetch_league_data()
    fetch_season_data()
    fetch_country_data()

if __name__ == "__main__":
    main()

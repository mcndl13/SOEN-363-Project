import requests
import json

# Function to fetch data from API and save it to a file
def fetch_data(url, headers, filename):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        with open(filename, "w") as file:
            file.write(response.text)
        print(f"Data has been written to {filename}")
    else:
        print(f"Failed to fetch data from {url}, Status Code: {response.status_code}")

# Method to fetch league data
def fetch_league_data():
    url = "https://v3.football.api-sports.io/leagues"
    headers = {
        'x-rapidapi-host': "v3.football.api-sports.io",
        'x-rapidapi-key': "62774e0697625ad93954c668d07ac020"
    }
    fetch_data(url, headers, "leagues.json")

# Method to fetch season data
def fetch_season_data():
    url = "https://v3.football.api-sports.io/leagues/seasons"
    headers = {
        'x-rapidapi-host': "v3.football.api-sports.io",
        'x-rapidapi-key': "62774e0697625ad93954c668d07ac020"
    }
    fetch_data(url, headers, "seasons.json")

# Method to fetch country data
def fetch_country_data():
    url = "https://v3.football.api-sports.io/countries"
    headers = {
        'x-rapidapi-host': "v3.football.api-sports.io",
        'x-rapidapi-key': "62774e0697625ad93954c668d07ac020"
    }
    fetch_data(url, headers, "countries.json")

    
def fetch_league_data2():
    url = "https://free-api-live-football-data.p.rapidapi.com/football-get-all-leagues-with-countries"
    headers = {
        'x-rapidapi-host': "free-api-live-football-data.p.rapidapi.com",
        'x-rapidapi-key': "433c6bdd7fmshf10677331de36dap176b31jsn51a9b86bc9ea"
    }
    fetch_data(url, headers, "leagues.json")

def main():
    # Fetching data
    # fetch_league_data()
    # fetch_season_data()
    # fetch_country_data()
    fetch_league_data2()

if __name__ == "__main__":
    main()

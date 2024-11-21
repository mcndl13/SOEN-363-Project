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

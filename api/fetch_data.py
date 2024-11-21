import requests


# Fetch league data

url = "https://v3.football.api-sports.io/leagues"

headers = {
    'x-rapidapi-host': "v3.football.api-sports.io",
    'x-rapidapi-key': "62774e0697625ad93954c668d07ac020"
}

response = requests.get(url, headers=headers)

with open("leagues.json", "w") as file:
    file.write(response.text)


# Fetch season data

url = "https://v3.football.api-sports.io/leagues/seasons"

headers = {
	"x-rapidapi-host": "v3.football.api-sports.io",
	"x-rapidapi-key": "62774e0697625ad93954c668d07ac020"
}

response = requests.get(url, headers=headers)

with open("seasons.json", "w") as file:
    file.write(response.text)

# Fetch country data

url = "https://v3.football.api-sports.io/countries"

headers = {
	"x-rapidapi-host": "v3.football.api-sports.io",
	"x-rapidapi-key": "62774e0697625ad93954c668d07ac020"
}

response = requests.get(url, headers=headers)

with open("countries.json", "w") as file:
    file.write(response.text)
import requests

url = "https://api-football-v1.p.rapidapi.com/v3/players/profiles"

headers = {
	"x-rapidapi-key": "2f59023b7emsh37f0abcdaa2852ap121f0cjsnf4d3d497819b",
	"x-rapidapi-host": "api-football-v1.p.rapidapi.com"
}

response = requests.get(url, headers=headers)

print(response.json())
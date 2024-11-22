import requests

url = "https://free-api-live-football-data.p.rapidapi.com/football-players-search"

querystring = {"search":"m"}

headers = {
	"x-rapidapi-key": "2f59023b7emsh37f0abcdaa2852ap121f0cjsnf4d3d497819b",
	"x-rapidapi-host": "free-api-live-football-data.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

print(response.json())
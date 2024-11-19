import requests

url = "https://free-api-live-football-data.p.rapidapi.com/football-get-list-all-team"

querystring = {"leagueid":"42"}

headers = {
	"x-rapidapi-key": "397db05a70msha1c30e10fb13342p107ec9jsn69f97db5281d",
	"x-rapidapi-host": "free-api-live-football-data.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

print(response.json())
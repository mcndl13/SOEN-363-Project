import requests

url = "https://v3.football.api-sports.io/leagues"

headers = {
    'x-rapidapi-host': "v3.football.api-sports.io",
    'x-rapidapi-key': "62774e0697625ad93954c668d07ac020"
}

response = requests.get(url, headers=headers)

# Save the response content to a file because to large for terminal (testing)
with open("leagues.json", "w") as file:
    file.write(response.text)

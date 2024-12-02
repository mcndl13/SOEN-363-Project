# Adjusting scale for faster generation but still aiming for large datasets
# Reduce entries: players (50k), matches (30k), stats (30k)

# Generate `players.csv` with 50,000 players
players = []
for player_id in range(1, 50001):  # 50,000 players
    team_id = np.random.choice(teams_df["teamid"])
    players.append([player_id, np.random.randint(1, 100), fake.word().capitalize(), fake.last_name(), fake.first_name(),
                    np.random.randint(18, 40), fake.country(), team_id])
players_df = pd.DataFrame(players, columns=["playerid", "jerseynumber", "position", "lastname", "firstname", "age", "nationality", "teamid"])

# Generate `matches.csv` with 30,000 matches
matches = []
for match_id in range(1, 30001):  # 30,000 matches
    home_team = np.random.choice(teams_df["teamid"])
    away_team = np.random.choice(teams_df["teamid"])
    while away_team == home_team:  # Ensure home and away teams are different
        away_team = np.random.choice(teams_df["teamid"])
    season_id = np.random.choice(seasons_df["seasonid"])
    result = np.random.choice(["Home", "Away", "Draw"])
    winner_team = home_team if result == "Home" else (away_team if result == "Away" else None)
    matches.append([match_id, fake.date_between(start_date="-5y", end_date="today"), home_team, away_team, season_id, 
                    result, winner_team, fake.city(), fake.word().capitalize() + " Stadium"])
matches_df = pd.DataFrame(matches, columns=["matchid", "date", "hometeamid", "awayteamid", "seasonid", "result", "winnerteamid", "city", "venue"])

# Generate `stats.csv` for 30,000 matches
stats = []
for stat_id in range(1, 30001):  # Stats for 30,000 matches
    match_id = stat_id  # Assuming one-to-one with matches
    stats.append([stat_id, match_id, np.random.randint(30, 70), np.random.randint(30, 70),
                  np.random.randint(0, 20), np.random.randint(0, 20), 
                  np.random.randint(0, 15), np.random.randint(0, 15),
                  np.random.randint(0, 15), np.random.randint(0, 15),
                  np.random.randint(0, 20), np.random.randint(0, 20)])
stats_df = pd.DataFrame(stats, columns=["statid", "matchid", "possessionhome", "possessionaway", "shotsontargethome", 
                                        "shotsontargetaway", "shotsofftargethome", "shotsofftargetaway", "cornershome", 
                                        "cornersaway", "foulshome", "foulsaway"])

# Save all data to CSV
output_path = "/mnt/data/"
teams_df.to_csv(output_path + "teams.csv", index=False)
leagues_df.to_csv(output_path + "league.csv", index=False)
seasons_df.to_csv(output_path + "season.csv", index=False)
teamleagues_df.to_csv(output_path + "teamleagues.csv", index=False)
players_df.to_csv(output_path + "players.csv", index=False)
matches_df.to_csv(output_path + "matches.csv", index=False)
stats_df.to_csv(output_path + "stats.csv", index=False)

output_path

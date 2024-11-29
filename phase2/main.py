from clear_db import clear_database
from load_league import load_league
from load_seasons import load_seasons
from load_teams import load_teams
from load_external_team_mapping import load_external_team_mapping
from load_team_leagues import load_team_leagues
from load_matches import load_matches
from load_players import load_players
from load_match_statistics import load_match_statistics

def main():
    # Clear the database
    clear_database()

    # File paths
    league_file =           "/Users/mohamedgueye/Documents/Concordia/Fall 2024/SOEN 363/SOEN-363-Project/phase 2/CSV/league.csv"
    season_file =           "/Users/mohamedgueye/Documents/Concordia/Fall 2024/SOEN 363/SOEN-363-Project/phase 2/CSV/seasons.csv"
    teams_file =            "/Users/mohamedgueye/Documents/Concordia/Fall 2024/SOEN 363/SOEN-363-Project/phase 2/CSV/teams.csv"
    mappings_file =         "/Users/mohamedgueye/Documents/Concordia/Fall 2024/SOEN 363/SOEN-363-Project/phase 2/CSV/external.csv"
    matches_file =          "/Users/mohamedgueye/Documents/Concordia/Fall 2024/SOEN 363/SOEN-363-Project/phase 2/CSV/matches.csv"
    players_file =          "/Users/mohamedgueye/Documents/Concordia/Fall 2024/SOEN 363/SOEN-363-Project/phase 2/CSV/players.csv"
    team_leagues_file =     "/Users/mohamedgueye/Documents/Concordia/Fall 2024/SOEN 363/SOEN-363-Project/phase 2/CSV/teamleagues.csv"
    match_statistics_file = "/Users/mohamedgueye/Documents/Concordia/Fall 2024/SOEN 363/SOEN-363-Project/phase 2/CSV/stats.csv"

    # Load data
    load_league(league_file)
    load_seasons(season_file)
    load_teams(teams_file)
    load_external_team_mapping(mappings_file)
    load_team_leagues(team_leagues_file)
    load_matches(matches_file)
    load_players(players_file)
    load_match_statistics(match_statistics_file)

    print("Data successfully loaded into Neo4j!")

if __name__ == "__main__":
    main()

from create_tables import create_tables
from fetch_leagues_and_seasons import fetch_and_insert_leagues_and_seasons
from fetch_teams import fetch_and_insert_teams
from fetch_matches import fetch_and_insert_matches
from fetch_players import fetch_and_insert_players
from fetch_match_statistics import fetch_and_insert_match_statistics
from goalkeeper import populate_goalkeeper_stats
from defender import populate_defender_stats

if __name__ == "__main__":
    # Create tables
    create_tables()

    # Populate leagues, seasons and teams table
    fetch_and_insert_leagues_and_seasons()
    fetch_and_insert_teams()

    # Populate matches and players
    fetch_and_insert_matches()
    fetch_and_insert_players()

    # Populate match statistics
    fetch_and_insert_match_statistics()

    # Populate position-specific tables
    populate_goalkeeper_stats()
    populate_defender_stats()
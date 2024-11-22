from create_tables import create_tables
from fetch_leagues_and_seasons import fetch_and_insert_leagues_and_seasons
from fetch_teams import fetch_and_insert_teams
from fetch_matches import fetch_and_insert_matches
from fetch_players import fetch_and_insert_players
from fetch_match_statistics import fetch_and_insert_match_statistics
from goalkeeper import populate_goalkeeper_stats  # Import for populating Goalkeeper table
from defender import populate_defender_stats  # Import for populating Defender table

if __name__ == "__main__":
    # Step 1: Create database tables
    create_tables()

    # Step 2: Populate foundational data
    fetch_and_insert_leagues_and_seasons()
    fetch_and_insert_teams()

    # Step 3: Insert matches and players
    fetch_and_insert_matches()
    fetch_and_insert_players()

    # Step 4: Insert match statistics
    fetch_and_insert_match_statistics()

    # Step 5: Populate position-specific tables
    populate_goalkeeper_stats()  # Populate stats for goalkeepers
    populate_defender_stats()  # Populate stats for defenders

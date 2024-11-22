from create_tables import create_tables
from fetch_leagues_and_seasons import fetch_and_insert_leagues_and_seasons
from fetch_teams import fetch_and_insert_teams
from fetch_matches import fetch_and_insert_matches
from fetch_players import fetch_and_insert_players
from fetch_match_statistics import fetch_and_insert_match_statistics

if __name__ == "__main__":
    create_tables()
    fetch_and_insert_leagues_and_seasons()
    fetch_and_insert_teams()
    fetch_and_insert_matches()
    fetch_and_insert_players()
    fetch_and_insert_match_statistics()

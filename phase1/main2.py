# Second API code

from create_tables import create_tables
from API2_fetch_leagues_and_seasons import fetch_and_insert_leagues_and_seasons
from API2_fetch_teams import fetch_and_insert_teams
from API2_fetch_players import fetch_and_insert_players


if __name__ == "__main__":
    # # Step 1: Create database tables
    # create_tables()

    # # Step 2: Populate foundational data
    # fetch_and_insert_leagues_and_seasons()

    # fetch_and_insert_teams()
    fetch_and_insert_players() 



# size of a db queries

# SELECT pg_size_pretty(pg_database_size('test'));
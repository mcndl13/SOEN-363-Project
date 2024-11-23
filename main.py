from create_tables import create_tables
from API2_fetch_leagues_and_seasons import fetch_and_insert_leagues_and_seasons
from API2_fetch_teams import fetch_and_insert_teams


if __name__ == "__main__":
    # # Step 1: Create database tables
    # create_tables()

    # # Step 2: Populate foundational data
    # fetch_and_insert_leagues_and_seasons()

    fetch_and_insert_teams() 
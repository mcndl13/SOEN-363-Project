# Phase 2 - Neo4j Data Loading

## Overview

The `phase2` folder contains scripts to load soccer-related data into a Neo4j database. The data includes leagues, seasons, teams, players, matches, and match statistics. The data is read from CSV files and loaded into the Neo4j database using the `py2neo` library.

## Folder Structure

- `CSV/`: Contains the CSV files with the data to be loaded.
- `clear_db.py`: Script to clear the Neo4j database.
- `env_setup.py`: Script to set up the environment and connect to the Neo4j database.
- `load_league.py`: Script to load league data into the Neo4j database.
- `load_seasons.py`: Script to load season data into the Neo4j database.
- `load_teams.py`: Script to load team data into the Neo4j database.
- `load_external_team_mapping.py`: Script to load external team mappings into the Neo4j database.
- `load_team_leagues.py`: Script to load team-league relationships into the Neo4j database.
- `load_matches.py`: Script to load match data into the Neo4j database.
- `load_players.py`: Script to load player data into the Neo4j database.
- `load_match_statistics.py`: Script to load match statistics into the Neo4j database.
- `main.py`: Main script to orchestrate the loading of all data into the Neo4j database.
- `utils.py`: Utility script with helper functions, such as loading CSV files.

## How to Use

1. **Set Up Environment**:
   - Ensure you have a Neo4j database running and accessible.
   - Create a `.env` file in the `phase2` folder with the following variables:
     ```
     BOLT_URL=bolt:
     USERNAME=neo4j
     PASSWORD=your_password
     ```

2. **Prepare CSV Files**:
   - Place the CSV files with the required data in the `CSV/` folder. The expected files are:
     - `league.csv`
     - `seasons.csv`
     - `teams.csv`
     - `external.csv`
     - `teamleagues.csv`
     - `matches.csv`
     - `players.csv`
     - `stats.csv`

3. **Run the Main Script**:
   - Execute the `main.py` script to load all data into the 

## Scripts Description

- **clear_db.py**: Clears all nodes and relationships in the Neo4j database.
- **env_setup.py**: Sets up the connection to the Neo4j database using environment variables.
- **load_league.py**: Loads league data from `CSV/league.csv` into the Neo4j database.
- **load_seasons.py**: Loads season data from `CSV/seasons.csv` into the Neo4j database.
- **load_teams.py**: Loads team data from `CSV/teams.csv` into the Neo4j database.
- **load_external_team_mapping.py**: Loads external team mappings from `CSV/external.csv` into the Neo4j database.
- **load_team_leagues.py**: Loads team-league relationships from `CSV/teamleagues.csv` into the Neo4j database.
- **load_matches.py**: Loads match data from `CSV/matches.csv` into the Neo4j database.
- **load_players.py**: Loads player data from `CSV/players.csv` into the Neo4j database.
- **load_match_statistics.py**: Loads match statistics from `CSV/stats.csv` into the Neo4j database.
- **main.py**: Orchestrates the loading of all data by calling the appropriate scripts in sequence.
- **utils.py**: Contains utility functions, such as `load_csv(filepath)` to read CSV files.

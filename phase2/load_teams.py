from py2neo import Node
from env_setup import graph
from utils import load_csv
from tqdm import tqdm  # Importing tqdm for the progress bar

def load_teams(filepath):
    data = load_csv(filepath)
    if not data:
        return

    for row in tqdm(data, desc="Loading Teams", unit="team"):
        try:
            # Handle team_id and founded_year, checking for 'NULL' or non-numeric values
            team_id = row["teamid"]
            founded_year = row["foundedyear"]

            # Handle 'NULL' or invalid team_id
            if team_id == 'NULL' or not team_id.isdigit():
                team_id = None  

            # Handle 'NULL' or invalid founded_year
            if founded_year == 'NULL' or not founded_year.isdigit():
                founded_year = None 

            # Convert valid team_id and founded_year to integers, leave them as None if invalid
            team_id = int(team_id) if team_id else None
            founded_year = int(founded_year) if founded_year else None

            # Now create the node
            team = Node(
                "Team",
                team_id=team_id,
                name=row["teamname"],
                founded_year=founded_year,
                country=row["country"]
            )

            # Merge the node with the graph
            graph.merge(team, "Team", "team_id")
        
        except Exception as e:
            print(f"Error loading team {row.get('teamname')}: {e}")
    
    print("Teams loaded successfully.")

from env_setup import graph

# Clear the entire database
def clear_database():
    try:
        graph.run("MATCH (n) DETACH DELETE n")
        print("Database cleared.")
    except Exception as e:
        print(f"Error clearing database: {e}")

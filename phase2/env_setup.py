import os
from dotenv import load_dotenv
from py2neo import Graph

# Load environment variables
load_dotenv()

# Retrieve Neo4j connection details from the environment
BOLT_URL = os.getenv("BOLT_URL")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

# Connect to the Neo4j database
graph = Graph(BOLT_URL, auth=(USERNAME, PASSWORD))

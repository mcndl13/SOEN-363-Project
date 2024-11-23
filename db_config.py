import psycopg2

DB_CONFIG = {
    "dbname": "dbname",
    "user": "user",
    "password": "XXXXX",
    "host": "host",
    "port": "5432",
}

def get_connection():
    try:
        return psycopg2.connect(**DB_CONFIG)
    except Exception as e:
        print(f"Error connecting to the database: {e}")

import psycopg2

DB_CONFIG = {
    "dbname": "test2",
    "user": "postgres",
    "password": "",
    "host": "localhost",
    "port": "5433",
}

def get_connection():
    try:
        return psycopg2.connect(**DB_CONFIG)
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None
import psycopg2

DB_CONFIG = {
    "dbname": "derien",
    "user": "postgres",
    "password": "HelloWorld101",
    "host": "localhost",
    "port": 5432
}

def get_connection():
    return psycopg2.connect(**DB_CONFIG)

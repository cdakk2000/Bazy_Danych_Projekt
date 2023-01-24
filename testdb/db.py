from dotenv import load_dotenv
import os
import psycopg2

def connect():
    """
    Connect to database and return connection
    """
    try:
        load_dotenv()
        conn = psycopg2.connect(
            host=os.getenv("POSTGRES_HOST"),
            dbname=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            port=os.getenv("POSTGRES_PORT")
        )
    except psycopg2.OperationalError as e:
        print(f"Could not connect to Database: {e}")
        exit(1)

    return conn

#!/usr/bin/env python3
from dotenv import load_dotenv
import psycopg2
import os

def connect():
    """
    Connect to database and return connection
    """
    print("Connecting to PostgreSQL Database...")
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

if __name__ == "__main__":
    conn = connect()
    with conn.cursor() as crsr:
        with open("tables.sql") as f:
            crsr.execute(f.read())
    conn.commit()

    exit(0)

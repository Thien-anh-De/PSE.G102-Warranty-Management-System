
import os
from pathlib import Path

import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv


ROOT_DIR = Path(__file__).resolve().parents[2]

load_dotenv(ROOT_DIR / ".env")


def get_connection():

    return psycopg.connect(
        host=os.getenv("DB_HOST", "127.0.0.1"),
        port=int(os.getenv("DB_PORT", "5433")),
        dbname=os.getenv("DB_NAME", "warranty_db"),
        user=os.getenv("DB_USER", "warranty_user"),
        password=os.environ["DB_PASSWORD"],
        connect_timeout=5,
        row_factory=dict_row
    )


def check_connection():

    with get_connection() as conn:

        with conn.cursor() as cursor:

            cursor.execute("""
                SELECT
                    current_database() AS database_name,
                    current_user AS username,
                    inet_server_port() AS port,
                    version() AS server_version
            """)

            return cursor.fetchone()


if __name__ == "__main__":

    try:

        result = check_connection()

        print("DATABASE CONNECTION SUCCESSFUL")

        for key, value in result.items():
            print(f"{key}: {value}")

    except Exception as error:

        print("DATABASE CONNECTION FAILED")
        print(error)

        raise SystemExit(1)

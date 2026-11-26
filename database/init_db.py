
from pathlib import Path

from src.warranty_core.database import get_connection


DATABASE_DIR = Path(__file__).resolve().parent

SQL_FILES = [
    "schema.sql",
    "ticket_schema.sql",
    "repair_schema.sql",
    "inventory_schema.sql",
    "management_schema.sql",
    "views.sql",
    "functions.sql",
    "triggers.sql",
    "inventory_functions.sql"
]


def initialize_database():

    print("Initializing PostgreSQL database...")

    with get_connection() as conn:

        result = conn.execute("""
            SELECT COUNT(*) AS total
            FROM pg_catalog.pg_tables
            WHERE schemaname = 'public'
        """).fetchone()

        if result["total"] > 0:

            print("Database already contains tables.")
            print("Initialization cancelled.")
            print("Existing data has not been modified.")

            return False

        conn.execute("SET LOCAL search_path TO public")

        for file_name in SQL_FILES:

            file_path = DATABASE_DIR / file_name

            if not file_path.exists():
                raise FileNotFoundError(
                    f"Missing SQL file: {file_name}"
                )

            print(f"Executing: {file_name}")

            sql_content = file_path.read_text(
                encoding="utf-8"
            )

            conn.execute(
                sql_content,
                prepare=False
            )

            print(f"SUCCESS: {file_name}")

        result = conn.execute("""
            SELECT COUNT(*) AS total
            FROM information_schema.tables
            WHERE table_schema = 'public'
                AND table_type = 'BASE TABLE'
        """).fetchone()

        total_tables = result["total"]

        if total_tables != 21:

            raise RuntimeError(
                f"Expected 21 tables, found {total_tables}"
            )

    print("=" * 50)
    print("DATABASE INITIALIZATION SUCCESSFUL")
    print(f"Total tables: {total_tables}")
    print("=" * 50)

    return True


if __name__ == "__main__":

    try:

        if not initialize_database():
            raise SystemExit(1)

    except Exception as error:

        print("DATABASE INITIALIZATION FAILED")
        print(error)

        raise SystemExit(1)

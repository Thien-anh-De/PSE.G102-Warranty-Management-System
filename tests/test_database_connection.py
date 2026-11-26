
import pytest

from src.warranty_core.database import get_connection


@pytest.mark.integration
def test_database_connection():

    with get_connection() as conn:

        with conn.cursor() as cursor:

            cursor.execute("SELECT 1 AS result")

            result = cursor.fetchone()

            assert result["result"] == 1


@pytest.mark.integration
def test_database_name():

    with get_connection() as conn:

        with conn.cursor() as cursor:

            cursor.execute("""
                SELECT current_database() AS database_name
            """)

            result = cursor.fetchone()

            assert result["database_name"] == "warranty_db"


@pytest.mark.integration
def test_database_user():

    with get_connection() as conn:

        with conn.cursor() as cursor:

            cursor.execute("""
                SELECT current_user AS username
            """)

            result = cursor.fetchone()

            assert result["username"] == "warranty_user"

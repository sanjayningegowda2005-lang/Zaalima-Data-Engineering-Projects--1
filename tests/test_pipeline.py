import os
import sqlite3
import pytest

DB_PATH = "pipeline_staging.db"


def test_database_file_exists():
    """Verify that the staging database file exists after ETL execution."""
    assert os.path.exists(
        DB_PATH
    ), f"Database file {DB_PATH} not found. Run main.py first."


def test_product_revenue_view_has_data():
    """Verify that the view_product_revenue view exists and is populated."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Verify view exists
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='view' AND name='view_product_revenue';"
    )
    view = cursor.fetchone()
    assert view is not None, "View 'view_product_revenue' does not exist in staging DB."

    # Verify view has rows
    cursor.execute("SELECT COUNT(*) FROM view_product_revenue;")
    count = cursor.fetchone()[0]
    conn.close()

    assert count > 0, "View 'view_product_revenue' is empty."
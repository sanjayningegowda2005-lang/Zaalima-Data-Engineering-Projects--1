from slalchemy import create_engine
def get_sqlite_engine(db_path=""):
    """
    Create a SQLAlchemy engine for SQLite database.

    :param db_path: Path to the SQLite database file.
    :return: SQLAlchemy engine instance.
    """
    engine = create_engine(f'sqlite:///{db_path}')
    return engine
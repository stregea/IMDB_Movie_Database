from interface.dbconn import DB
from utils.globals import DATABASE
from .tables import CREATE_TABLE_LIST


def initialise_database() -> None:
    """
    Initialize the database upon initial startup.
    """
    db = DB(DATABASE)
    for create_table in CREATE_TABLE_LIST:
        db.commit(create_table)
    db.close()


if __name__ == '__main__':
    initialise_database()

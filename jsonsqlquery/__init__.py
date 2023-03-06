import sqlite3

from jsonsqlquery import core


def query(in_data: core.Data, query: str) -> core.Data:
    connection = sqlite3.connect(":memory:")
    keys_to_data_types = core.get_keys_and_data_types(in_data)
    core.create_db_and_insert(connection, in_data, keys_to_data_types)
    return core.query_db(connection, query)

import numbers
import typing as t


Data = list[dict[str, t.Any]]


def get_keys_and_data_types(in_data: Data) -> dict[str, str]:
    keys = list(in_data[0].keys())
    data_types = {key: infer_data_type(in_data, key) for key in keys}
    return data_types


def infer_data_type(in_data: Data, key: str) -> str:
    non_null_values = [row[key] for row in in_data if row[key] is not None]
    if not non_null_values:
        return "NULL"
    elif all([isinstance(v, (bool, int)) for v in non_null_values]):
        return "INTEGER"
    elif all([isinstance(v, numbers.Number) for v in non_null_values]):
        return "REAL"
    return "TEXT"


def create_db_and_insert(connection, in_data: Data, keys_to_data_types: dict[str, str]):
    cursor = connection.cursor()

    create_table_sql = f""" 
CREATE TABLE data (
    {",".join(f"{key} {data_type}" for key, data_type in keys_to_data_types.items())}  
)"""
    cursor.execute(create_table_sql)

    for in_row in in_data:
        insert_row_sql = f"""
INSERT INTO data (
    {",".join(keys_to_data_types)}
) VALUES (
    {",".join(["?"] * len(keys_to_data_types))}
)"""
        cursor.execute(insert_row_sql, [in_row[key] for key in keys_to_data_types])
        connection.commit()


def query_db(connection, query: str) -> Data:
    cursor = connection.cursor()
    cursor.execute(query)
    out_keys: list[str] = [d[0] for d in cursor.description]
    out_data: Data = []
    for row in cursor.fetchall():
        out_data.append(dict(zip(out_keys, row)))
    return out_data

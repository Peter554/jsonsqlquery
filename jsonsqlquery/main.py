import sys
import pathlib
import json
import numbers
import argparse
import sqlite3
import typing as t

Data = list[dict[str, t.Any]]


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("--query")
    arg_parser.add_argument("--query-file")
    arg_parser.add_argument("--create-db")
    args = arg_parser.parse_args()

    if args.create_db and pathlib.Path(args.create_db).exists():
        raise Exception(f"{args.create_db} already exists.")
    connection = sqlite3.connect(args.create_db or ":memory:")

    in_data, keys, data_types = get_in_data()

    create_db_and_insert(connection, in_data, keys, data_types)

    if args.create_db:
        return

    query = get_query(args)
    out_data = query_db(connection, query)
    for row in out_data:
        print(json.dumps(row))


def get_query(args: t.Any) -> str:
    if args.query is not None:
        return args.query
    elif args.query_file is not None:
        with open(args.query_file) as f:
            return f.read()
    else:
        raise Exception("Please provide a query.")


def get_in_data() -> tuple[Data, list[str], dict[str, str]]:
    in_data: Data = []
    for row in sys.stdin:
        if not row.strip():
            continue
        in_data.append(json.loads(row))
    keys = list(in_data[0].keys())
    data_types = {key: infer_data_type(in_data, key) for key in keys}
    return in_data, keys, data_types


def infer_data_type(in_data: Data, key: str) -> str:
    non_null_values = [row[key] for row in in_data if row[key] is not None]
    if not non_null_values:
        return "NULL"
    elif all([isinstance(v, (bool, int)) for v in non_null_values]):
        return "INTEGER"
    elif all([isinstance(v, numbers.Number) for v in non_null_values]):
        return "REAL"
    return "TEXT"


def create_db_and_insert(connection, in_data, keys, data_types):
    cursor = connection.cursor()

    create_table_sql = f""" 
CREATE TABLE data (
    {",".join(f"{key} {data_types[key]}" for key in keys)}  
)"""
    cursor.execute(create_table_sql)

    for in_row in in_data:
        insert_row_sql = f"""
INSERT INTO data (
    {",".join(keys)}
) VALUES (
    {",".join(["?"] * len(keys))}
)"""
        cursor.execute(insert_row_sql, [in_row[key] for key in keys])
        connection.commit()


def query_db(connection, query) -> Data:
    cursor = connection.cursor()
    cursor.execute(query)
    out_keys: list[str] = [d[0] for d in cursor.description]
    out_data: Data = []
    for row in cursor.fetchall():
        out_data.append(dict(zip(out_keys, row)))
    return out_data


if __name__ == "__main__":
    main()

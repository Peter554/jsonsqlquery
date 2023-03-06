import sys
import pathlib
import json
import argparse
import sqlite3
import typing as t

from jsonsqlquery import core


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("--query")
    arg_parser.add_argument("--query-file")
    arg_parser.add_argument("--create-db")
    args = arg_parser.parse_args()

    if args.create_db and pathlib.Path(args.create_db).exists():
        raise Exception(f"{args.create_db} already exists.")
    connection = sqlite3.connect(args.create_db or ":memory:")

    in_data = get_in_data()
    keys_to_data_types = core.get_keys_and_data_types(in_data)

    core.create_db_and_insert(connection, in_data, keys_to_data_types)

    if args.create_db:
        return

    query = get_query(args)
    out_data = core.query_db(connection, query)
    for row in out_data:
        print(json.dumps(row))


def get_in_data() -> core.Data:
    in_data: core.Data = []
    for row in sys.stdin:
        if not row.strip():
            continue
        in_data.append(json.loads(row))
    return in_data


def get_query(args: t.Any) -> str:
    if args.query is not None:
        return args.query
    elif args.query_file is not None:
        with open(args.query_file) as f:
            return f.read()
    else:
        raise Exception("Please provide a query.")


if __name__ == "__main__":
    main()

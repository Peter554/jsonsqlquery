# jsonsqlquery

[![CI](https://github.com/Peter554/jsonsqlquery/actions/workflows/ci.yml/badge.svg)](https://github.com/Peter554/jsonsqlquery/actions/workflows/ci.yml)

Query JSON using SQL.

```
pip install jsonsqlquery
```

## Examples

```
# students.jsonl
{"name": "Alvin", "age": 25, "major": "Literature"}
{"name": "Kathy", "age": 31, "major": "Literature"}
{"name": "Pauline", "age": 11, "major": "Mathematics"}
{"name": "Nora", "age": 27, "major": "Mathematics"}
{"name": "Martin", "age": 54, "major": "Geology"}
```

Inline SQL query:

```
cat students.jsonl | jsonsqlquery --query 'select name, age from data where age > 30'
```

SQL query from a file:

```
cat students.jsonl | jsonsqlquery --query-file query.sql
```

Create a SQLite database:

```
cat students.jsonl | jsonsqlquery --create-db students.db
```

See the `examples/` directory.

## Caveats

* Booleans are cast to integers.
* Data is assumed to fit in memory.

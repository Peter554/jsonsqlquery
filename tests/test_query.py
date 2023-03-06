from jsonsqlquery import query


def test_query():
    in_data = [
        {"name": "Alvin", "age": 25, "major": "Literature"},
        {"name": "Kathy", "age": 31, "major": "Literature"},
        {"name": "Pauline", "age": 11, "major": "Mathematics"},
        {"name": "Nora", "age": 27, "major": "Mathematics"},
        {"name": "Martin", "age": 54, "major": "Geology"},
    ]

    assert query(
        in_data,
        "select name, age from data where age > 30",
    ) == [
        {"name": "Kathy", "age": 31},
        {"name": "Martin", "age": 54},
    ]

    assert query(
        in_data,
        "select major, count(*) count from data group by major",
    ) == [
        {"major": "Geology", "count": 1},
        {"major": "Literature", "count": 2},
        {"major": "Mathematics", "count": 2},
    ]

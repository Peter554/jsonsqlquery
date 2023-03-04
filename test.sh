cat examples/in_data.jsonl | poetry run python jsonquery/main.py --query-file examples/query_1.sql > /tmp/out_data.jsonl
cmp /tmp/out_data.jsonl examples/out_data_1.jsonl

cat examples/in_data.jsonl | poetry run python jsonquery/main.py --query-file examples/query_2.sql > /tmp/out_data.jsonl
cmp /tmp/out_data.jsonl examples/out_data_2.jsonl

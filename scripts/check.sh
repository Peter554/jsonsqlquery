set -e

poetry run black --check .

poetry run mypy . 

scripts/test.sh
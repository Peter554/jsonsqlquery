set -e

poetry run black --check .

poetry run mypy . 

poetry run pytest

export PYTHONPATH=$PWD
scripts/clitest.sh
# Generate dataset and SQL queries

Run commands from the repository root (`quartz/`).

## Setup

```bash
source setup.sh
```

## Requirements
```bash
pip3 install pybars3
pip3 install pyyaml
```

## SQL queries (YAML)

```bash
python3 generator/python/main.py sql
python3 generator/python/main.py sql -s examples/db/sqlite.sql -o examples/db
```

## Dataset

```bash
# Schema
python3 generator/python/main.py ds

# Python
python3 generator/python/main.py ds python -s examples/db/sqlite.sql -o examples/python/ds
python3 generator/python/main.py ds python -s examples/db/sqlite.sql -o examples/python/ds -b -d -a

# PHP
python3 generator/python/main.py ds php -s examples/db/sqlite.sql -o examples/php/ds -n books -b -d -a
```

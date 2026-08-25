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
python3 generator/python/main.py sql -s examples/db/books.sql -o examples/db
```

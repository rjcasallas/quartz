# Quartz Examples

## SQL

```bash
# Queries
python generator/python/main.py sql -s examples/db/sqlite.sql -o examples/db
```

## Python

### Generate
```bash
# Dataset
python generator/python/main.py ds python -s examples/db/sqlite.sql -o examples/python/ds
python generator/python/main.py ds python -s examples/db/sqlite.sql -o examples/python/ds -r -m -q -x -a
```

### Examples
```bash
# Main
python examples/python/main.py
python examples/python/main.py red -c 1

# Tests
python examples/python/test.py

# Dataset
python examples/python/data.py
```

## PHP

### Generate
```bash
# Dataset
python3 generator/python/main.py ds php -s examples/db/sqlite.sql -o examples/php/ds -b -d -a
```

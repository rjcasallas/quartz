# Quartz Examples

## SQL

```bash
# Queries
python generator/python/main.py sql -s examples/db/books.sql -o examples/db
```

## Python

### Generate
```bash
# Dataset
python generator/python/main.py ds python -s examples/db/books.sql -o examples/python/ds
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

# Testing in the project running on Docker

## Creating tests

- Use naming conventions established in [unittest -documentation](https://docs.python.org/3/library/unittest.html#basic-example)
- If you create sub-folders to tests/, make sure to add `__init__.py` so that the tests are found by discover command

## Running tests

### Run all pytests

```
docker compose run --rm test
```

### Run pytests without playwright

```
docker compose run --rm test --ignore=tests/playwright/
```

### Run only only playwright tests

```
docker compose run --rm test tests/playwright/ --browser chromium
```

### Run pytests with coverage HTML report

```
docker compose run --rm test --cov=src --cov-report=html
```

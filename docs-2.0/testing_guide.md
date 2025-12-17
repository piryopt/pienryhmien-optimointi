# Testing in the project running on Docker

## Creating tests

- Use naming conventions established in [unittest -documentation](https://docs.python.org/3/library/unittest.html#basic-example)
- If you create sub-folders to tests/, make sure to add `__init__.py` so that the tests are found by discover command

## Getting started

Build the test service. This will take a while due to the large playwright image. You only need to build this once.

```
docker compose build test
```

To run playwright tests you also need to build web-test image with.

```
docker compose build web-test
```

This will build a react dist and run flask for E2E testing. You need to rebuild this service if you make changes to frontend.

## Running tests

### Run all pytests

```
docker compose run --rm test
```

### Run pytests without playwright

```
docker compose run --rm test --ignore=tests/playwright/
```

### Run only playwright tests

```
docker compose run --rm test tests/playwright/ --browser chromium
```

### Run pytests with coverage HTML report

```
docker compose run --rm test --cov=src --cov-report=html
```

### Run vitests and get coverage

Go to frontend directory and run:

```
npm run test -- --coverage
```

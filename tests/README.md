# Tests

## Creating tests
- Use naming conventions established in [unittest -documentation](https://docs.python.org/3/library/unittest.html#basic-example)
- If you create sub-folders to tests/, make sure to add ```__init__.py``` so that the tests are found by discover command

## Running tests

### Run all discovered tests
```
> python3 -m coverage run --source=. -m unittest discover
```

### Running code coverage
```
> python3 -m coverage report
```

### Generating a HTML-coverage report 
```
> python3 -m coverage html
```
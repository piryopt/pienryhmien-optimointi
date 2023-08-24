


# Testing instructions

## Local testing

**Download the code and install dependencies**

Download the code from top right corner button: Code > Download ZIP. Extract the zip file to your computer. Open the terminal and navigate to the application files folder. Create a virtual environment and go there with the following command:

```bash
poetry shell
```
Install the dependencies:

```bash
poetry install
```

**Create local database**

Open new tab in terminal and create the local database.

'''bash
pg_ctl start
psql
CREATE DATABASE choose-name-for-DB;
'''

Copy the contenst from [schema.sql](https://github.com/piryopt/pienryhmien-optimointi/blob/main/schema.sql) to the terminal.

**Start the application**

Return to the first tab in Terminal. Start the application:

```bash
flask run
```


## Unit tests

Run Unittests:

```bash
poetry run pytest
```

Test coverage report:

```bash
coverage run --branch -m pytest
coverage report -m
```


## Ui tests (Robot Framework)

```bash
robot tests
```
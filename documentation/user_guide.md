# User guide for Jakaja
Jakaja is an application for assigning large numbers of students into groups. This user guide helps you set up Jakaja locally and to test using it.

### Local use

#### First time set up
Download source code, for example by choosing "Code" > "Download ZIP" on the github repository page and then unzip the downloaded file.

Check that a current version of Python is downloaded and set up. Python can be downloaded for example [here](https://www.python.org/downloads/).

Check that PostgreSQL is downloaded and set up. It can be downloaded [from the PostgreSQL web page](https://www.postgresql.org/download/) or if you're using a University of Helsinki Cubbli system, you can use [this script](https://github.com/hy-tsoha/local-pg/tree/master)

Create a file called ".env" to the app root folder and add the following contents
```bash
DATABASE_URL="postgresql:///user"
SECRET_KEY ="key"
```
Here in place of user add your username in the system and in place of "key" add a token you can create for example with the following commands in a terminal

```bash
python3
>>> import secrets
>>> secrets.token_hex(16)
```

Jakaja uses [Poetry](https://python-poetry.org/) to manage dependencies. Download Poetry, for example with Linux or macOS you can use the following command in a terminal

```bash
curl -sSL https://install.python-poetry.org | POETRY_HOME=$HOME/.local python3 -
```

Navigate to the Jakaja app root folder on your terminal

Install the dependencies with
```bash
poetry install
```

Activate Poetry environment
```bash
poetry shell
```

Have your database running in the backgroud.

Return to the terminal with your virtual environment and set up the database schema with
```bash
psql < schema.sql
```

Run app
```bash
flask run
```

Enter the app by navigating to  http://127.0.0.1:5000 on your browser or by clicking the link appearing in your terminal


#### Using the app after first time set up
Activate database in the background.

In a new terminal window activate the virtual environment
```bash
source venv/bin/activate
```

Run app
```bash
flask run
```

Enter the app by navigating to  http://127.0.0.1:5000 on your browser or by clicking the link appearing in your terminal

#### Closing the app

You can close the project by closing the browser window, using "control+C" in your terminal and deactivating the virtual environment with
```bash
exit
```
Remember to also close the database connection.
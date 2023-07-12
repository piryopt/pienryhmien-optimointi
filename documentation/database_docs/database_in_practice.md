# How to use the databases in different environments
The easiest way to make changes to the database is to use Postgres terminal, here is the explanation how to do it

## Test and Production servers
The database has its own container in Openshift and you can access its terminal

Test and Production database urls and passwords can be found in their respective Openshift environments in the Secrets tab.

## Locally
Some people have downloaded Postgres differently so this may not work, but it worked for us

- Open your Postgres terminal, for us psql postgres or psql template1 or psql your_username worked
- create database chosen_name; creates an empty database. \c chosen_name connects you to the database
- Copy and paste the text from schema.sql to psql terminal creates the tables. You can use \dt to see the tables in the current database
- Create file a named .env to the project root and add it to .gitignore. Your milage may vary, but for us adding this line to .env worked fine
'''
DATABASE_URL=postgresql:///chosen_name
'''
- You are good to go (hopefully)
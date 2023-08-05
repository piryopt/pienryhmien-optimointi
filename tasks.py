from invoke import task

# call poetry run invoke robots db_name
@task
def robots(ctx, db_name):
    ctx.run(f"psql {db_name} < drop.sql && psql {db_name} < schema.sql && robot -d logs tests/survey_testing.robot", pty=True)

@task
def headless(ctx, db_name):
    ctx.run(f"psql {db_name} < drop.sql && psql {db_name} < schema.sql && robot -d logs tests/headless_testing.robot", pty=True)

@task
def staging(ctx):
    ctx.run("robot -d logs tests/staging_testing.robot", pty=True)

@task
def clear(ctx):
    ctx.run("rm logs/*", pty=True)

from invoke import task

# call poetry run invoke robots db_name
@task
def robots(ctx, db_name):
    ctx.run(f"robot -d logs tests/survey_testing.robot && psql {db_name} < drop.sql && psql {db_name} < schema.sql", pty=True)

@task
def staging(ctx):
    ctx.run("robot -d logs tests/staging_testing.robot", pty=True)

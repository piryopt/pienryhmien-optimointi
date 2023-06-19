from invoke import task


@task
def robots(ctx):
    ctx.run("robot -d logs tests", pty=True)

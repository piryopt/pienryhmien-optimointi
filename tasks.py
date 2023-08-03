from invoke import task


@task
def robots_teacher(ctx):
    ctx.run("robot -d logs tests/teacher_testing.robot", pty=True)

@task
def robots_student(ctx):
    ctx.run("robot -d logs tests/student_testing.robot", pty=True)

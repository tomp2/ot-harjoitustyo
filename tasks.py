import platform

from invoke import task

USE_PTY: bool = platform.system() == "Linux"


@task
def start(ctx):
    ctx.run("python3 src/skilltracker/index.py", pty=USE_PTY)


@task(aliases=("tests",))
def test(ctx):
    ctx.run("pytest src/tests", pty=USE_PTY)


@task
def coverage(ctx):
    ctx.run("coverage run --branch -m pytest src/skilltracker", pty=USE_PTY)


def coverage_report(ctx):
    ctx.run("coverage report -m", pty=USE_PTY)


@task(coverage)
def coverage_html(ctx):
    ctx.run("coverage html", pty=USE_PTY)


@task(aliases=("format",))
def black(ctx):
    ctx.run("black ./", pty=USE_PTY)


@task
def mypy(ctx):
    ctx.run("mypy src/skilltracker", pty=USE_PTY)


@task(aliases=("lint",))
def pylint(ctx):
    ctx.run("pylint src/skilltracker", pty=USE_PTY)

import nox


PYTHON_FILES = [
    "setup.py",
    "suorafxctl.py",
    "noxfile.py",
]


@nox.session(reuse_venv=True)
def lint(session):
    session.install("flake8", "black")
    session.run("black", "--check", "--diff", "--color", *PYTHON_FILES)
    session.run("flake8", *PYTHON_FILES)


@nox.session(reuse_venv=True)
def black_fix(session):
    session.install("black")
    session.run("black", *PYTHON_FILES)

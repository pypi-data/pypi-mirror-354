# wirepy/migrations.py

import subprocess

def run_migrate(name="auto"):
    subprocess.run(["alembic", "revision", "--autogenerate", "-m", name])

def run_upgrade():
    subprocess.run(["alembic", "upgrade", "head"])

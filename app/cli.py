import os
import click
from app import db, app


def register(app):
    @app.cli.command()
    def init():
        print("initializing database")
        os.system("flask db init")
        os.system("flask db migrate")
        os.system("flask db upgrade")
        os.system("python -m app.populate")

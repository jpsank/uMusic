from app import app, db, cli
from app.models import Track, Album, Artist

cli.register(app)


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Track': Track, 'Album': Album, 'Artist': Artist}


if __name__ == '__main__':
    app.run()

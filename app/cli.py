import os
import click


def register(cli):

    @cli.command()
    def init():
        print("initializing database")
        os.system("flask db init")
        os.system("flask db migrate")
        os.system("flask db upgrade")
        os.system("python -m app.populate")

    @cli.command()
    @click.option('--genre', default='danceedm', help='genre of music to scrape')
    @click.argument('count')
    def scrape(genre, count):
        from app.scrape import soundcloud
        soundcloud.download_charts(genre=genre, limit=count)

    @cli.command()
    def populate():
        from app.populate import populate
        populate.add_tracks_recur()


@click.group()
def main_cli():
    pass


if __name__ == '__main__':
    register(main_cli)
    main_cli()

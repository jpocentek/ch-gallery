import click

from flask import current_app, g
from flask.cli import with_appcontext
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from chgallery.db.declarative import Base


def create_db_engine():
    # SQLite engine
    return create_engine('sqlite:///{}'.format(current_app.config['DATABASE']))

    # MySQL engine
    # engine = create_engine('mysqlclient+mysql://dbuser:dbpass@localhost')
    # engine.execute('USE dbname')
    # return engine

    # PostgreSQL engine
    # return create_engine('postgresql+psycopg2://dbuser:dbpass@localhost/dbname')


def create_db_session(engine):
    DBSession = sessionmaker(bind=create_db_engine())
    return DBSession()


def get_db_session():
    if 'db_session' not in g:
        g.db_session = create_db_session(create_db_engine())
    return g.db_session


def close_db(e=None):
    session = g.pop('db_session', None)
    if session is not None:
        session.close()
        session.bind.dispose()


def init_db():
    engine = create_db_engine()
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    engine.dispose()


@click.command('init-db')
@with_appcontext
def init_db_command():
    """ Clear the existing data and create new tables """
    init_db()
    click.echo('Initialized the database')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

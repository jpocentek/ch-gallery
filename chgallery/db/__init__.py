import click
from flask import current_app, g
from flask.cli import with_appcontext
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from chgallery.db.declarative import Base


def create_db_engine():
    """
    Creates new engine to be used by SQLAlchemy depending on database
    configuration. Connection string is taken directly from application
    configuration so it must be provided as required by SQLAlchemy.

    Note that to use anything other than Sqlite you have to install
    appropriate database driver by yourself. Check SQLAlchemy docs
    for all information.

    Possible db settings:

    * Sqlite:     'sqlite:///path_to_db.sqlite'
    * MySQL:      'mysql+mysqlconnector://chester:233mmx@localhost/chester'
    * PostgreSQL: 'postgresql+psycopg2://dbuser:dbpass@localhost/dbname'
    """
    return create_engine(current_app.config['DATABASE'])


def get_db_session():
    """
    Creates new DB session if it does not exist in scope of
    current application. Otherwise returns existing session.
    """
    if 'db_session' not in g:
        g.db_session = sessionmaker(bind=create_db_engine())()
    return g.db_session


def close_db(e=None):
    """
    Closess database session and removes all engine bindings.
    """
    session = g.pop('db_session', None)
    if session is not None:
        session.close()
        session.bind.dispose()


def init_db():
    """
    Remove existing tables from database and create
    new in initial state. This should be used after
    every fresh installation.
    """
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

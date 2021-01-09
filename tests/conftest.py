import json
import os
import shutil
import tempfile
from collections import namedtuple

import pytest
from werkzeug.security import generate_password_hash

from chgallery import create_app
from chgallery.db import get_db_session, init_db
from chgallery.db.declarative import Album, Image, User

__FAKE_DATA_FILE__ = os.path.join(os.getcwd(), 'tests', 'fixtures', 'data.json')

DataItem = namedtuple('DataItem', ['classname', 'key'])


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()
    upload_path = tempfile.mkdtemp('upload')

    app = create_app({
        'TESTING': True,
        'DATABASE': 'sqlite:///{}'.format(db_path),
        'UPLOAD_PATH': upload_path,
        'WTF_CSRF_ENABLED': False,

        # https://stackoverflow.com/questions/31766082/flask-url-for-error-attempted-to-generate-a-url-without-the-application-conte # noqa
        'SERVER_NAME': 'localhost.localdomain',
    })

    # Create test user as it's required for almost all views
    test_user = User(
        username='test',
        password=generate_password_hash('test'),
        email='test@example.com',
    )

    with app.app_context():
        init_db()
        db_session = get_db_session()
        db_session.add(test_user)
        db_session.commit()
        db_session.close()

    yield app

    os.close(db_fd)
    os.unlink(db_path)
    shutil.rmtree(upload_path)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


class AuthActions:

    def __init__(self, app, client):
        self._app = app
        self._client = client

    def login(self, username='test', password='test'):
        data = {
            'username': username,
            'password': password,
        }

        return self._client.post('/auth/login', data=data)

    def logout(self):
        return self._client.get('/auth/logout')


@pytest.fixture
def auth(app, client):
    return AuthActions(app, client)


@pytest.fixture
def load_fake_data(app):
    with app.app_context():
        db_session = get_db_session()

    with open(__FAKE_DATA_FILE__, 'r') as fp:
        fake_data = json.loads(fp.read())

    for data_item in (
                DataItem(classname=User, key='users'),
                DataItem(classname=Album, key='albums'),
                DataItem(classname=Image, key='images'),
            ):
        for item in [data_item.classname(**x) for x in fake_data[data_item.key]]:
            db_session.add(item)
        db_session.commit()

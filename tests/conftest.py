import os
import shutil
import tempfile

import pytest
from werkzeug.security import generate_password_hash

from chgallery import create_app
from chgallery.db import get_db_session, init_db
from chgallery.db.declarative import User


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()
    upload_path = tempfile.mkdtemp('upload')

    app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
        'UPLOAD_PATH': upload_path,
        # https://stackoverflow.com/questions/31766082/flask-url-for-error-attempted-to-generate-a-url-without-the-application-conte # noqa
        'SERVER_NAME': 'localhost.localdomain',
        'WTF_CSRF_ENABLED': False,
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

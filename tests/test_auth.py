import pytest

from chgallery.db import get_db_session
from chgallery.db.declarative import User


class TestLoginForm:
    _login_url = '/auth/login'
    _redirect_url = '/auth/'

    def test_login(self, client, auth):
        assert client.get(self._login_url).status_code == 200
        response = auth.login()
        assert response.headers['location'].endswith(self._redirect_url)

    def test_login_failed(self, client):
        assert client.get(self._login_url).status_code == 200
        data = {
            'username': 'doesnotexist',
            'password': 'wrongpassword',
        }
        response = client.post(self._login_url, data=data)
        assert b'Invalid login credentials' in response.data

    # TODO: better authentication mechanism. For now it's risky
    # to determine in login view if user is already authenticated.
    #
    # Status: Failing
    # def test_redirect_logged_user(self, client, auth):
    #     auth.login()
    #     response = client.get(self._login_url)
    #     assert response.headers['location'] == self._redirect_url


class TestRegisterForm:
    _register_url = '/auth/register'

    def test_register_while_disabled(self, app, client):
        app.config['REGISTRATION_DISABLED'] = True
        assert client.get(self._register_url).status_code == 404

    def test_register(self, app, client):
        assert client.get(self._register_url).status_code == 200
        data = {
            'username': 'otheruser',
            'email': 'otheruser@example.com',
            'password': 'otherpassword',
            'password_repeat': 'otherpassword',
        }
        response = client.post(self._register_url, data=data)
        assert response.headers['location'].endswith('/auth/login')
        with app.app_context():
            db_session = get_db_session()
            # We'll get an error if user does not exist
            db_session.query(User).filter(User.username == 'otheruser').one()
            db_session.close()

    @pytest.mark.parametrize(('username', 'email', 'password', 'password_repeat', 'message'), (
        ('', '', '', '', b'This field is required'),
        ('otheruser', '', '', '', b'This field is required'),
        ('otheruser', 'otheruser@example.com', '', '', b'This field is required'),
        ('otheruser', 'otheruser@example.com', 'somepassword', '', b'Field must be equal to password'),
        ('test', 'otheruser@example.com', 'somepassword', '', b'User test already exists'),
        ('otheruser', 'test@example.com', 'somepassword', '', b'Email already taken'),
    ))
    def test_register_failed(self, client, username, email, password, password_repeat, message):
        data = {
            'username': username,
            'email': email,
            'password': password,
            'password_repeat': password_repeat,
        }
        response = client.post(self._register_url, data=data)
        assert message in response.data


def test_logout(client, auth):
    auth.login()
    assert client.get('/auth/').status_code == 200
    auth.logout()
    response = client.get('/auth/')
    assert response.headers['location'].endswith('/auth/login')


def test_login_required_decorator(client, auth):
    response = client.get('/auth/')
    assert response.headers['location'].endswith('/auth/login')
    auth.login()
    assert client.get('/auth/').status_code == 200

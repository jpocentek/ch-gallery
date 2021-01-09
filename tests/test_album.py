import pytest
from sqlalchemy.orm.exc import NoResultFound

from chgallery.db import get_db_session
from chgallery.db.declarative import Album


__URLCONFIG__ = {
    'album_list': '/album/',
    'album_delete': '/album/{album_id}/delete',
    'login_redirect': '/auth/login',
}


class TestAlbumListClass:

    def test_anonymous_user_cannot_access_album_list(self, client):
        response = client.get(__URLCONFIG__['album_list'])
        assert response.status_code == 302
        assert response.headers['location'].endswith(__URLCONFIG__['login_redirect'])

    def test_authorized_user_can_access_album_list(self, auth, client):
        auth.login()
        assert client.get(__URLCONFIG__['album_list']).status_code == 200


class TestAlbumDeleteClass:

    def test_delete_returns_404_if_object_does_not_exist(self, app, auth, client):
        auth.login()
        url = __URLCONFIG__['album_delete'].format(album_id=1)
        assert client.post(url).status_code == 404

    def test_unauthorized_user_cannot_access_delete_view(self, client):
        response = client.post(__URLCONFIG__['album_delete'].format(album_id=1))
        assert response.status_code == 302
        assert response.headers['location'].endswith(__URLCONFIG__['login_redirect'])

    def test_only_owner_can_delete_album(self, auth, client, load_fake_data):
        auth.login('otheruser', 'otherpass')
        response = client.post(__URLCONFIG__['album_delete'].format(album_id=1))
        assert response.status_code == 403

    def test_successful_album_delete_action(self, app, auth, client, load_fake_data):
        auth.login()
        response = client.post(__URLCONFIG__['album_delete'].format(album_id=1))
        assert response.status_code == 302
        assert response.headers['location'].endswith(__URLCONFIG__['album_list'])

        with app.app_context():
            db_session = get_db_session()

        with pytest.raises(NoResultFound):
            db_session.query(Album).filter(Album.id == 1).one()

import pytest
from sqlalchemy.orm.exc import NoResultFound

from chgallery.db import get_db_session
from chgallery.db.declarative import Album


__URLCONFIG__ = {
    'album_list': '/album/',
    'album_create': '/album/create',
    'album_update': '/album/{album_id}/update',
    'album_delete': '/album/{album_id}/delete',
    'album_add_images': '/album/{album_id}/images/add',
    'album_update_images': '/album/{album_id}/images/update',

    'image_list': '/image/',

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


class TestAlbumCreateClass:

    def test_anonymous_user_cannot_access_album_create_form(self, client):
        response = client.get(__URLCONFIG__['album_create'])
        assert response.status_code == 302
        assert response.headers['location'].endswith(__URLCONFIG__['login_redirect'])

    def test_authorized_user_can_access_album_create_form(self, auth, client):
        auth.login()
        response = client.get(__URLCONFIG__['album_create'])
        assert response.status_code == 200

    @pytest.mark.parametrize(('name', 'description', 'message'), (
        ('', '', b'This field is required'),
        ('xtLCv0FQk.z.e:TnKmm$bI#jWE~y8QyWC', '', b'Field cannot be longer than 32 characters'),
        ('Album Name', '~qI>h%A7DeLA2J<8;O3yU<lpei=m4fvG%$PT$JeDGH1ItQkOxi9eU7F*7OMW>ei;yKMhr%Rrj4euxPoU:2bqbDWB>Jj6f$waxbPt,lKDlxgSdb0Zypk:w:itCh~yd<.CoG3rsRVeWAjALET%R7E9;v~vr:~oc9ONI.k=n<:am%FFvr.ros%>iwVu.AoDgIDmCY&PR$6UK5BFtZi:zT~dT**63bd9Y=C8L;qUd.JcQekBl*ue=Ky*S0LEXjJAQ2au', b'Field cannot be longer than 255 characters'),  # noqa
    ))
    def test_form_validation_with_invalid_data(self, auth, client, name, description, message):
        auth.login()
        data = {'name': name, 'description': description}
        response = client.post(__URLCONFIG__['album_create'], data=data)
        assert response.status_code == 200
        assert message in response.data

    def test_successful_album_creation(self, app, auth, client):
        auth.login()
        data = {'name': "Test Album 1", 'description': "Test Album Description"}
        response = client.post(__URLCONFIG__['album_create'], data=data)
        assert response.status_code == 302
        assert response.headers['location'].endswith(__URLCONFIG__['album_list'])

        with app.app_context():
            db_session = get_db_session()

        instance = db_session.query(Album).filter(Album.author_id == 1).one()
        assert instance.name == "Test Album 1"
        assert instance.description == "Test Album Description"


class TestAlbumUpdateClass:

    def test_update_returns_404_if_object_does_not_exist(self, app, auth, client):
        auth.login()
        url = __URLCONFIG__['album_update'].format(album_id=1)
        assert client.post(url).status_code == 404

    def test_unauthorized_user_cannot_access_update_view(self, client):
        response = client.post(__URLCONFIG__['album_update'].format(album_id=1))
        assert response.status_code == 302
        assert response.headers['location'].endswith(__URLCONFIG__['login_redirect'])

    def test_only_owner_can_update_album(self, auth, client, load_fake_data):
        auth.login('otheruser', 'otherpass')
        response = client.post(__URLCONFIG__['album_update'].format(album_id=1))
        assert response.status_code == 403

    def test_that_field_values_are_filled_from_model_fields(self, auth, client, load_fake_data):
        auth.login()
        response = client.get(__URLCONFIG__['album_update'].format(album_id=1))
        assert response.status_code == 200
        assert b'value="Album 1"' in response.data
        assert b'value="This is for testing only"' in response.data

    def test_successful_album_update(self, app, auth, client, load_fake_data):
        auth.login()

        data = {'name': 'Updated Name', 'description': 'Updated description'}
        response = client.post(__URLCONFIG__['album_update'].format(album_id=1), data=data)
        assert response.status_code == 302
        assert response.headers['location'].endswith(__URLCONFIG__['album_list'])

        with app.app_context():
            db_session = get_db_session()

        obj = db_session.query(Album).filter(Album.id == 1).one()
        assert obj.name == 'Updated Name'
        assert obj.description == 'Updated description'


class TestAlbumDeleteClass:

    def test_delete_returns_404_if_object_does_not_exist(self, auth, client):
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


class TestAddImagesToAlbumClass:

    def test_unauthorized_user_cannot_access_add_images_view(self, client, load_fake_data):
        url = __URLCONFIG__['album_add_images'].format(album_id=1)
        response = client.post(url)
        assert response.status_code == 302
        assert response.headers['location'].endswith(__URLCONFIG__['login_redirect'])

    def test_add_images_returns_404_if_album_does_not_exist(self, auth, client):
        auth.login()
        url = __URLCONFIG__['album_add_images'].format(album_id=1)
        assert client.post(url).status_code == 404

    def test_add_images_returns_404_if_image_does_not_exist(self, auth, client, load_fake_data):
        auth.login()
        url = __URLCONFIG__['album_add_images'].format(album_id=1)
        data = {'images': [9999]}  # Ensure that image ID does not exist
        assert client.post(url, data=data).status_code == 404

    def test_only_album_owner_can_add_images(self, auth, client, load_fake_data):
        auth.login()
        url = __URLCONFIG__['album_add_images'].format(album_id=2)
        assert client.post(url).status_code == 403

    def test_only_image_owner_can_add_images(self, auth, client, load_fake_data):
        auth.login()
        url = __URLCONFIG__['album_add_images'].format(album_id=1)
        data = {'images': [2]}  # Image does not belong to authorized user

        # Here we'll return 404 response as we want to only select images belonging to
        # authorized user. It's obvious that selected id/author_id combination does
        # not exist if user is not an image owner.
        assert client.post(url, data=data).status_code == 404

    def test_image_successfully_added_with_image_add_view(self, app, auth, client, load_fake_data):
        auth.login()

        album_id = 1
        image_id = 1

        url = __URLCONFIG__['album_add_images'].format(album_id=album_id)
        data = {'images': [image_id]}  # Image does not belong to authorized user

        response = client.post(url, data=data)
        assert response.status_code == 302
        assert response.headers['location'].endswith(__URLCONFIG__['image_list'])

        with app.app_context():
            db_session = get_db_session()

        obj = db_session.query(Album).filter(Album.id == album_id).one()
        assert image_id in [x.id for x in obj.images]
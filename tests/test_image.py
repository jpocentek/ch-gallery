import io
import os

from werkzeug.datastructures import FileStorage

from chgallery.db import get_db_session
from chgallery.db.declarative import Image


def test_only_authorized_user_can_upload_file(client):
    data = {'file': (io.BytesIO(b'Hello, world!'), 'example.txt')}
    response = client.post('/image/upload', data=data)
    assert response.status_code == 302
    assert response.headers['location'].endswith('/auth/login')


def test_upload_with_wrong_mime_type(client, auth):
    auth.login()
    mock_file = FileStorage(
        stream=io.BytesIO(b'Hello, world!'),
        filename='example.txt',
        content_type='text/plain',
    )
    response = client.post(
        '/image/upload',
        data={'image': mock_file},
        content_type='multipart/form-data',
    )
    assert b'An image of type' in response.data


def test_successful_upload(app, client, auth):
    auth.login()
    test_picture = os.path.join(os.getcwd(), 'tests', 'test_picture.jpg')
    mock_file = FileStorage(
        stream=open(test_picture, 'rb'),
        filename='test_picture.jpg',
        content_type='image/jpeg',
    )
    data = {
        'image': mock_file,
        'description': 'Test Image',
    }
    client.post('/image/upload', data=data)
    with app.app_context():
        db_session = get_db_session()
        image = db_session.query(Image).filter(Image.name == 'test_picture.jpg').one()
        db_session.close()
        assert image.description == 'Test Image'
        assert image.url().endswith('/image/uploads/{}'.format(image.name))
        assert image.thumbnail_url().endswith('/image/uploads/thumbs/{}'.format(image.name))

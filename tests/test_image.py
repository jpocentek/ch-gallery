import io
import os

import pytest
from PIL import Image as PILImage
from werkzeug.datastructures import FileStorage

from chgallery.db import get_db_session
from chgallery.db.declarative import Image
from chgallery.image.utils import is_allowed_image_file, smart_resize

TEST_PICTURE = os.path.join(os.getcwd(), 'tests', 'test_picture.jpg')


@pytest.fixture
def mock_txt_file():
    return FileStorage(
        stream=io.BytesIO(b'Hello, world!'),
        filename='example.txt',
        content_type='text/plain',
    )


@pytest.fixture
def mock_jpg_file():
    return FileStorage(
        stream=open(TEST_PICTURE, 'rb'),
        filename='test_picture.jpg',
        content_type='image/jpeg',
    )


@pytest.fixture
def image_copy():
    """ Copy original picture for safety """
    img = PILImage.open(TEST_PICTURE)
    img_copy = img.copy()
    img.close()
    return img_copy


def test_image_validation_with_invalid_file(mock_txt_file):
    assert not is_allowed_image_file(mock_txt_file)


def test_image_validation_with_valid_image(mock_jpg_file):
    assert is_allowed_image_file(mock_jpg_file)


def test_resize_wide_image(image_copy):
    image_copy = smart_resize(image_copy)
    assert image_copy.width == 2000
    assert image_copy.height == 1333


def test_resize_high_image(image_copy):
    # Rotate image by 90 degrees and swap width and height
    image_copy = image_copy.rotate(90, expand=1)
    image_copy = smart_resize(image_copy)
    assert image_copy.height == 2000
    assert image_copy.width == 1333


def test_only_authorized_user_can_upload_file(client):
    response = client.post('/image/upload', data={'image': mock_txt_file})
    assert response.status_code == 302
    assert response.headers['location'].endswith('/auth/login')


def test_upload_with_wrong_mime_type(client, auth, mock_txt_file):
    auth.login()
    response = client.post(
        '/image/upload',
        data={'image': mock_txt_file},
        content_type='multipart/form-data',
    )
    assert b'An image of type' in response.data


def test_successful_upload(app, client, auth, mock_jpg_file):
    auth.login()
    data = {
        'image': mock_jpg_file,
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
        assert image.name in os.listdir(app.config['UPLOAD_PATH'])
        assert image.name in os.listdir(os.path.join(app.config['UPLOAD_PATH'], 'thumbs'))

    response = client.get('/image/uploads/{}'.format(image.name))
    assert response.status_code == 200
    assert response.headers['content-type'] == 'image/jpeg'

    response = client.get('/image/uploads/thumbs/{}'.format(image.name))
    assert response.status_code == 200
    assert response.headers['content-type'] == 'image/jpeg'


def test_unique_name_creation(app, client, auth, mock_jpg_file):
    auth.login()

    for i in range(3):
        test_image = FileStorage(
            stream=open(TEST_PICTURE, 'rb'),
            filename='repeated_name.jpg',
            content_type='image/jpeg',
        )

        data = {
            'image': test_image,
            'description': 'Repeated name {}'.format(i),
        }

        client.post('/image/upload', data=data, content_type='multipart/form-data')

    with app.app_context():
        db_session = get_db_session()
        items = (
            db_session.query(Image)
            .filter(Image.name.like('repeated_name%'))
            .order_by(Image.id).all()
        )
        db_session.close()

    assert len(items) == 3
    assert items[0].name == 'repeated_name.jpg'
    assert items[1].name == 'repeated_name(1).jpg'
    assert items[2].name == 'repeated_name(2).jpg'

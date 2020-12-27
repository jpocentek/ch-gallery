import io
from werkzeug.datastructures import FileStorage


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

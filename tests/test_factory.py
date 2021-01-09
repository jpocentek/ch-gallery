from chgallery import create_app
from chgallery.db import get_db_session
from chgallery.db.declarative import Image


def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing


def test_index(app, client, load_fake_data):
    with app.app_context():
        db_session = get_db_session()

    assert len(db_session.query(Image).all()) == 2
    assert client.get('/').status_code == 200

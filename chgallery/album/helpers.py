from flask import (
    abort,
    g,
    request
)
from sqlalchemy.orm.exc import NoResultFound

from chgallery.db import get_db_session
from chgallery.db.declarative import Album


def get_album_instance(album_id):
    """
    Raises 404 response if instance with given ID could not be
    found in database or 403 if user is not an instance owner.
    Otherwise returns Album object instance.

    :param int: album_id Selected album instance ID

    :returns: Album object instance
    :rtype: chgallery.db.declarative.Album
    """
    db_session = get_db_session()

    try:
        obj = db_session.query(Album).filter(Album.id == album_id).one()
    except NoResultFound:
        abort(404)

    if obj.author_id != g.user.id:
        abort(403)

    return obj


def update_album_images(album_id, replace=False):
    """
    Validates POST data and updates album's images. If 'replace' is set
    to true, an entire new list of images will be saved. Otherwise selected
    images will be appended to already existing objects.

    If POST data is invalid, 400 response will be returned.

    :param int: album_id Album instance ID
    :param bool: replace If set to 'true', an entire list will be replaced
    """
    obj = get_album_instance(album_id)

    try:
        id_list = [int(x) for x in request.form.getlist('images')]
    except (TypeError, ValueError):
        # Form is not intended to be used directly by site user so
        # it's most likely that malformed data comes from some
        # unusual activity. So we do not bother to display exact errors.
        abort(400)

    selected_images = [x for x in g.user.images if x.id in id_list]

    if replace:
        obj.images = selected_images
    else:
        # If duplicated enties exists, they will be
        # removed with 'db_session.commit()' call.
        obj.images += selected_images

    db_session = get_db_session()
    db_session.commit()

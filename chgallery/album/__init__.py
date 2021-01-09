from flask import (
    Blueprint,
    abort,
    flash,
    g,
    redirect,
    render_template,
    url_for
)
from sqlalchemy.orm.exc import NoResultFound
from chgallery.auth.decorators import login_required
from chgallery.db import get_db_session
from chgallery.db.declarative import Album

bp = Blueprint('album', __name__, url_prefix='/album')


@bp.route('/', methods=('GET',))
@login_required
def album_list():
    """
    The main album management page. Presents list of all albums
    belonging to currently authorized user.
    """
    albums = (
        get_db_session().query(Album)
        .filter(Album.author_id == g.user.id)
        .all()
    )

    return render_template('album/index.html', albums=albums)


@bp.route('/<int:album_id>/delete', methods=('POST',))
@login_required
def album_delete(album_id):
    """ Delete selected album if authorized user is album's owner """
    db_session = get_db_session()

    try:
        instance = db_session.query(Album).filter(Album.id == album_id).one()
    except NoResultFound:
        abort(404)

    if instance.author != g.user:
        abort(403)

    db_session.delete(instance)
    db_session.commit()
    flash('Album deleted', 'danger')

    return redirect(url_for('album.album_list'))

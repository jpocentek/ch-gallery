from flask import (
    Blueprint,
    abort,
    flash,
    g,
    redirect,
    render_template,
    request,
    url_for
)
from sqlalchemy.orm.exc import NoResultFound
from chgallery.auth.decorators import login_required
from chgallery.db import get_db_session
from chgallery.db.declarative import Album

from .forms import AlbumForm

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


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def album_create():
    """ Create new album owned by currently authorized user """
    form = AlbumForm()

    if form.validate_on_submit():
        form.instance.author = g.user
        form.save()
        flash('New album created', 'success')
        return redirect(url_for('album.album_list'))

    return render_template('album/album_form.html', form=form)


@bp.route('/<int:album_id>/update', methods=('GET', 'POST'))
@login_required
def album_update(album_id):
    """ Update selected album if authorized user is album's owner """
    db_session = get_db_session()

    try:
        obj = db_session.query(Album).filter(Album.id == album_id).one()
    except NoResultFound:
        abort(404)

    if obj.author_id != g.user.id:
        abort(403)

    form = AlbumForm(instance=obj)

    if form.validate_on_submit():
        form.save()
        flash('Album updated', 'success')
        return redirect(url_for('album.album_list'))

    return render_template('album/album_form.html', form=form)


@bp.route('/<int:album_id>/delete', methods=('POST',))
@login_required
def album_delete(album_id):
    """ Delete selected album if authorized user is album's owner """
    db_session = get_db_session()

    try:
        obj = db_session.query(Album).filter(Album.id == album_id).one()
    except NoResultFound:
        abort(404)

    if obj.author_id != g.user.id:
        abort(403)

    db_session.delete(obj)
    db_session.commit()

    flash('Album deleted', 'danger')
    return redirect(url_for('album.album_list'))


@bp.route('/<int:album_id>/images/add', methods=('POST',))
@login_required
def album_images_add(album_id):
    """
    Add images to selected album. This view will usually be used
    to add single selected image on image list view but it actually
    accepts list of ID's of images to be added to album.
    """
    db_session = get_db_session()

    try:
        obj = db_session.query(Album).filter(Album.id == album_id).one()
    except NoResultFound:
        abort(404)

    if obj.author_id != g.user.id:
        abort(403)

    try:
        id_list = [int(x) for x in request.form.getlist('images')]
    except (TypeError, ValueError):
        # Form is not intended to be used directly by site user so
        # it's most likely that malformed data comes from some
        # unusual activity. So we do not bother to display exact errors.
        abort(400)

    obj.images += [x for x in g.user.images if x.id in id_list]
    db_session.commit()

    flash('Images added succesfully', 'success')
    return redirect(url_for('image.index'))


@bp.route('/<int:album_id>/images/update', methods=('GET', 'POST',))
@login_required
def album_images_update(album_id):
    """
    Lists all user's images with information if they're already included
    in selected album and allows to modify this list and save entirely
    new image list for selected album.
    """
    raise NotImplementedError

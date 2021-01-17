from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    url_for
)

from chgallery.auth.decorators import login_required
from chgallery.db import get_db_session
from chgallery.db.declarative import Album

from .forms import AlbumForm
from .helpers import get_album_instance, update_album_images

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
    obj = get_album_instance(album_id)
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
    obj = get_album_instance(album_id)

    db_session = get_db_session()
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
    update_album_images(album_id)
    return {'status': 'success'}


@bp.route('/<int:album_id>/images/update', methods=('GET', 'POST',))
@login_required
def album_images_update(album_id):
    """
    Lists all user's images with information if they're already included
    in selected album and allows to modify this list and save entirely
    new image list for selected album.
    """
    if request.method == 'POST':
        update_album_images(album_id, replace=True)
        flash('Album updated', 'success')
        return redirect(url_for('image.index'))
    else:
        obj = get_album_instance(album_id)
        return render_template('album/image_update.html', obj=obj, images=g.user.images)

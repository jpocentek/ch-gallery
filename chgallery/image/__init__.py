import os

from PIL import Image as PILImage
from flask import (
    Blueprint,
    abort,
    current_app,
    flash,
    g,
    send_from_directory,
    redirect,
    render_template,
    url_for
)
from sqlalchemy.orm.exc import NoResultFound
from werkzeug.utils import secure_filename

from chgallery.auth.decorators import login_required
from chgallery.db import get_db_session
from chgallery.db.declarative import Image

from chgallery.image.forms import UploadForm
from chgallery.image.utils import smart_resize


bp = Blueprint('image', __name__, url_prefix='/image')


def get_unique_filename(filename):
    """
    Create unique filename using given name to ensure that
    it's not already present in database. This method simply
    adds a counter to original filename.

    :param str filename:
    :rtype str:
    """
    filename = secure_filename(filename)
    final_name = filename
    db_session = get_db_session()
    success = False
    retries = 0

    while not success:
        try:
            db_session.query(Image).filter(Image.name == final_name).one()
            retries += 1
            fname, ext = os.path.splitext(filename)
            final_name = '{}({}){}'.format(fname, retries, ext)
        except NoResultFound:
            success = True

    return final_name


@bp.route('/', methods=('GET',))
@login_required
def index():
    """
    Presents images uploaded by currently authorized user and
    allows image manipulation (updating and deleting images).
    """
    images = (
        g.db_session.query(Image)
        .filter(Image.author == g.user)
        .order_by(Image.creation_date.desc())
    )

    return render_template('image/index.html', images=images)


@bp.route('/upload', methods=('GET', 'POST'))
@login_required
def upload():
    form = UploadForm()

    if form.validate_on_submit():
        image = Image(
            name=get_unique_filename(form.image.data.filename),
            description=form.description.data,
            author_id=g.user.id,
        )

        # Create normalized image and thumbnail
        img = PILImage.open(form.image.data)
        img = smart_resize(img)

        # Create new entry in database
        image.width, image.height = img.size
        db_session = get_db_session()
        db_session.add(image)
        db_session.commit()

        # Save both images - resized version and thumbnail
        img.save(os.path.join(current_app.config['UPLOAD_PATH'], image.name), img.format)
        img.thumbnail((250, 250))
        img.save(os.path.join(current_app.config['UPLOAD_PATH'], 'thumbs', image.name), img.format)
        img.thumbnail((100, 100))
        img.save(os.path.join(current_app.config['UPLOAD_PATH'], 'previews', image.name), img.format)

        flash('Image uploaded successfully', 'success')
        return redirect(url_for('auth.dashboard'))

    return render_template('image/upload.html', form=form)


@bp.route('/delete/<int:image_id>', methods=('POST',))
@login_required
def delete(image_id):
    db_session = get_db_session()

    try:
        obj = db_session.query(Image).filter(Image.id == image_id).one()
    except NoResultFound:
        abort(404)

    if obj.author != g.user:
        abort(403)

    # Remove files associated with Image object instance
    os.unlink(os.path.join(current_app.config['UPLOAD_PATH'], obj.name))
    os.unlink(os.path.join(current_app.config['UPLOAD_PATH'], 'thumbs', obj.name))
    os.unlink(os.path.join(current_app.config['UPLOAD_PATH'], 'previews', obj.name))

    # Remove Image instance from database
    db_session.delete(obj)
    db_session.commit()

    flash('Object removed', 'info')
    return redirect(url_for('auth.dashboard'))


def display_uploaded_file(filename, dirname=None):
    path = current_app.config['UPLOAD_PATH']
    if dirname is not None:
        path = os.path.join(path, dirname)
    return send_from_directory(path, filename)


@bp.route('/uploads/<filename>')
def uploaded_file(filename):
    return display_uploaded_file(filename)


@bp.route('/uploads/thumbs/<filename>')
def uploaded_file_thumbnail(filename):
    return display_uploaded_file(filename, 'thumbs')


@bp.route('/uploads/previews/<filename>')
def uploaded_file_preview(filename):
    return display_uploaded_file(filename, 'previews')

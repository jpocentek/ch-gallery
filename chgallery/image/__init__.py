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
from chgallery.image.utils import smart_resize, smart_thumbnail


bp = Blueprint('image', __name__, url_prefix='/image')


def get_unique_filename(filename):
    filename = secure_filename(filename)
    db_session = get_db_session()
    success = False
    retries = 0

    while not success:
        try:
            db_session.query(Image).filter(Image.name == filename).one()
            retries += 1
            fname, ext = os.path.splitext(filename)
            filename = '{}({}){}'.format(fname, retries, ext)
        except NoResultFound:
            success = True

    return filename


@bp.route('/upload', methods=('GET', 'POST'))
@login_required
def upload():
    form = UploadForm()

    if form.validate_on_submit():
        image = Image(
            name=get_unique_filename(form.image.data.filename),
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
        img = smart_thumbnail(img)
        img.save(os.path.join(current_app.config['UPLOAD_PATH'], 'thumbs', image.name), img.format)

        flash('Image uploaded successfully')
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

    # Remove Image instance from database
    db_session.delete(obj)
    db_session.commit()

    flash('Object removed')
    return redirect(url_for('auth.dashboard'))


@bp.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(current_app.config['UPLOAD_PATH'], filename)


@bp.route('/uploads/thumbs/<filename>')
def uploaded_file_thumbnail(filename):
    path = os.path.join(current_app.config['UPLOAD_PATH'], 'thumbs')
    return send_from_directory(path, filename)

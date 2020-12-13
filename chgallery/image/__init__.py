from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    url_for
)
from werkzeug.utils import secure_filename

from chgallery.auth.decorators import login_required
from chgallery.db import get_db_session
from chgallery.db.declarative import Image
from chgallery.image.forms import UploadForm


bp = Blueprint('image', __name__, url_prefix='/image')


@bp.route('/upload', methods=('GET', 'POST'))
@login_required
def upload():
    form = UploadForm()

    if form.validate_on_submit():
        image = Image(
            name=secure_filename(form.image.data.filename),
            author_id = g.user.id,
        )
        db_session = get_db_session()
        db_session.add(image)
        db_session.commit()
        flash('Image uploaded successfully')
        return redirect(url_for('auth.dashboard'))

    return render_template('image/upload.html', form=form)

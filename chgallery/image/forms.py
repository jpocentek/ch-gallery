from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField
from wtforms.validators import Length, StopValidation

from chgallery.image.utils import is_allowed_image_file


class ImageFileRequired(FileRequired):

    def __call__(self, form, field):
        super().__call__(form, field)
        if not is_allowed_image_file(field.data):
            raise StopValidation(
                "An image of type 'jpg', 'png' or 'gif' is required"
            )


class UploadForm(FlaskForm):
    image = FileField('image', validators=[ImageFileRequired()])
    description = StringField('description', validators=[Length(min=0, max=255)])

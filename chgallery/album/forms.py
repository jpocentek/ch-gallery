from wtforms import StringField
from wtforms.validators import DataRequired, Length

from chgallery.forms import ModelForm
from chgallery.db.declarative import Album


class AlbumForm(ModelForm):

    __model__ = Album

    name = StringField('name', validators=[DataRequired(), Length(max=32)])
    description = StringField('description', validators=[Length(max=255)])

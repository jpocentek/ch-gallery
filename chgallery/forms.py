from flask_wtf import FlaskForm
from chgallery.db import get_db_session


class FormNotValidatedError(Exception):
    message = (
        "Form not initialized. You must call either 'validate'"
        " or 'validate_on_submit' directly on Form instance."
    )

    def __init__(self, *args, **kwargs):
        super().__init__(self.message, *args, **kwargs)


class ModelForm(FlaskForm):

    def __init__(self, instance=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if instance is not None:
            self.instance = instance

    def save(self):
        db_session = get_db_session()
        db_session.add(self.instance)
        db_session.commit()
        db_session.flush()
        return self.instance

    def validate(self, *args, **kwargs):
        is_valid = super().validate(*args, **kwargs)

        if not is_valid:
            return is_valid

        attrs = {x: self.data[x] for x in self.data if x in self.__model__.__dict__}
        if not getattr(self, 'instance', None):
            self.instance = self.__model__(**attrs)
        else:
            self.instance.__dict__.update(**attrs)

        return is_valid

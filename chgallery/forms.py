from flask_wtf import FlaskForm
from chgallery.db import get_db_session


class FormNotValidatedError(Exception):
    """
    Raised when form is not validated and we try to get created instance.
    """
    message = (
        "Form not initialized. You must call either 'validate'"
        " or 'validate_on_submit' directly on Form instance."
    )

    def __init__(self, *args, **kwargs):
        super().__init__(self.message, *args, **kwargs)


class ModelForm(FlaskForm):
    """
    Form to be used directly with models of selected type.

    Classes inheriting from ModelForm must have '__model__' property declared. This property points
    to specific sqlalchemy.declarative.Base subclass.

    Model form may be instantiated without any arguments and in this case we'll work on creating new
    models instance. You can provide 'instance' argument when initializing model form and provided
    object instance will be updated.

    It's necessary to call 'validate' or 'validate_on_submit' method before operating directly on
    form's model instance.
    """

    def __init__(self, instance=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if instance is not None:
            self.instance = instance

            # Fill-in initial field values directly from model fields.
            # Skip this process if form is submitted - we take data from user instead.
            if not self.is_submitted():
                self._fill_initial_values()

    def _fill_initial_values(self):
        attrs = {k: v for k, v in self.instance.__dict__.items() if k in self.data.keys()}
        for k, v in attrs.items():
            field = getattr(self, k)
            field.data = v

    def save(self):
        """ Save new model instance or update existing row """
        db_session = get_db_session()

        if not self.instance.id:
            db_session.add(self.instance)

        db_session.commit()
        db_session.flush()

        return self.instance

    def validate(self, *args, **kwargs):
        """ Validate data and update model fields """
        is_valid = super().validate(*args, **kwargs)

        if not is_valid:
            return is_valid

        attrs = {x: self.data[x] for x in self.data if x in self.__model__.__dict__}
        if not getattr(self, 'instance', None):
            # new instance
            self.instance = self.__model__(**attrs)
        else:
            # update existing instance
            for k, v in attrs.items():
                setattr(self.instance, k, v)

        return is_valid

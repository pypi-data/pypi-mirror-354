# Third party
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

# gcloudc
from gcloudc.forms.fields import TrueOrNoneFormField


class TrueOrNoneField(models.BooleanField):
    """A Field only storing `None` or `True` values.

    Why? This allows unique_together constraints on fields of this type
    ensuring that only a single instance has the `True` value.

    It mimics a nullable BooleanField field in it's behaviour, while it will
    raise an exception when explicitly validated, assigning something
    unexpected (like a string) and saving, will silently convert that
    value to either True or None.
    """
    default_error_messages = {
        'invalid': _("'%s' value must be either True or None."),
    }
    description = _("Boolean (Either True or None)")

    def __init__(self, *args, **kwargs):
        kwargs = kwargs.copy()
        kwargs["null"] = True
        super().__init__(*args, **kwargs)

    def from_db_value(self, value, expression, connection):
        return self.to_python(value)

    def to_python(self, value):
        if value in (None, "None", False):
            return None
        if value in (True, "t", "True", "1"):
            return True
        msg = self.error_messages["invalid"] % str(value)
        raise ValidationError(msg)

    def get_prep_value(self, value):
        """Only ever save None's or True's in the db. """
        if not value:
            return None
        return True

    def formfield(self, **kwargs):
        defaults = {
            "form_class": TrueOrNoneFormField
        }
        defaults.update(kwargs)
        return super().formfield(**defaults)

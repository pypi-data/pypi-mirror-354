import copy

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.db.models.fields import (
    CharField,
    Field,
    BigAutoField,
    SmallAutoField
)

from django.db.models.fields import AutoFieldMixin, AutoFieldMeta


__all__ = (
    "AutoCharField",
    "MapField",
)


def _monkeypatched_get_subclasses(self):
    return (BigAutoField, SmallAutoField, AutoCharField)


class AutoCharField(AutoFieldMixin, CharField):
    _autofield_meta_monkeypatched = False

    @classmethod
    def _monkeypatch_autofield_meta(cls):
        """
        Monkeypatch AutoFieldMeta _subclasses property to include
        AutoField - this is so that isinstance(AutoCharField(), AutoField)
        passes without having to override all AutoField methods.
        """
        AutoFieldMeta._subclasses = property(_monkeypatched_get_subclasses)

    def __init__(self, *args, **kwargs):
        kwargs.pop("max_length", None)

        # Some django code (in particular SQLInsertCompiler.execute_sql)
        # in Django 5.2 onwards performs a "isinstance(field, AutoField)"
        # check. We cannot easily extends AutoField directly, as that
        # assumes an integer field. Instead, we monkeypatch AutoField metaclass
        # so that the isinstance check passes for instances of AutoCharField.
        # In future Django releases, there are plans to allow non-int autopk
        # through a Field attribute, at which point we can stop doing this
        if not AutoCharField._autofield_meta_monkeypatched:
            self._monkeypatch_autofield_meta()
            AutoCharField._autofield_meta_monkeypatched = True

        # We explicitly set a default of None, otherwise CharField uses a default
        # of an empty string and that's not a valid key
        kwargs.setdefault("default", None)

        super().__init__(max_length=1500, *args, **kwargs)

    def get_internal_type(self):
        return "AutoCharField"

    def rel_db_type(self, connection):
        return CharField().db_type(connection=connection)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs.pop("max_length")
        return name, path, args, kwargs


class MapField(Field):
    """
        This is a field that internally saves as a Firestore
        Map property. It takes an optional Model class which if
        specified is then used for field validation.
    """

    empty_strings_allowed = False
    empty_values = (None,)

    def __init__(self, model=None, *args, **kwargs):
        self._model = model
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs["model"] = self._model
        return (name, path, args, kwargs)

    def db_type(self, connection):
        return "map"

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value

        if self._model:
            loaded_values = {}
            for field in self._model._meta.fields:
                field_value = value.get(field.column)

                # Documentation says built in fields don't have this
                # function implemented for performance so we only call
                # it if it's there
                if hasattr(field, "from_db_value"):
                    field_value = field.from_db_value(field_value, expression, connection)

                loaded_values[field.attname] = field_value
            value = loaded_values

        return value

    def validate(self, value, model_instance):
        super().validate(value, model_instance)

        if self._model:
            # We need to validate the dictionary conforms to the model structure.
            # This calls clean, and will pass any unspecified fields as None, if those
            # fields aren't nullable then an error will be raised.
            model_fields = set([x.attname for x in self._model._meta.fields])
            input_fields = set(value.keys()) if value else set()
            if input_fields - model_fields:
                raise ValidationError(
                    f"Map property for model '{self._model}' defines extra field/s {input_fields - model_fields}"
                )

            for field in self._model._meta.fields:
                field_value = value.get(field.attname) if value else None
                if not field.null and field_value is None:
                    raise ValidationError(
                        "Map property '{}' cannot be None".format(field.attname)
                    )

                # This will raise a ValidationError if there's a problem
                if hasattr(field, "_model") and field_value:
                    field.validate(field_value, field._model)
                field_value = field.to_python(field_value)
                value[field.attname] = field_value

    def get_db_prep_value(self, value, connection, prepared=False):
        if prepared:
            return value
        value = super().get_db_prep_value(value, connection, prepared)
        if value is not None:
            return_value = {}
            if self._model:
                for field in self._model._meta.fields:
                    field_value = value.get(field.attname)
                    field_value = field.get_db_prep_value(field_value, connection, prepared)
                    return_value[field.column] = field_value
                value = return_value
        return value

    def pre_save(self, model_instance, add):
        try:
            data = self.value_from_object(model_instance)
            if data:
                if not isinstance(data, dict):
                    raise IntegrityError(
                        "{} cannot be a '{}'".format(self.attname, type(data))
                    )

                self.validate(data, model_instance)
        except ValidationError as e:
            raise IntegrityError from e

        return super().pre_save(model_instance, add)

    def get_lookup(self, lookup_name):
        LookupClass = super().get_lookup("exact")

        attname = self.attname

        class DynamicLookup(LookupClass):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)

                col = "{}.{}".format(attname, lookup_name)
                self.lhs = copy.deepcopy(self.lhs)
                self.lhs.field.column = col

        return DynamicLookup

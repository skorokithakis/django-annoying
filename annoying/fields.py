from django import VERSION

from django.db import models
from django.db.models import OneToOneField
from django.core.serializers.json import DjangoJSONEncoder
try:
    from django.db.models.fields.related import SingleRelatedObjectDescriptor
except ImportError:
    from django.db.models.fields.related_descriptors import ReverseOneToOneDescriptor as SingleRelatedObjectDescriptor
from django.utils import six

# South support.
try:
    from south.modelsinspector import add_introspection_rules
    SOUTH = True
except ImportError:
    SOUTH = False

# Try to be compatible with Django 1.5+.
try:
    import json
except ImportError:
    from django.utils import simplejson as json

# Basestring no longer exists in Python 3
try:
    basestring
except:
    basestring = str

try:
    from django.db.transaction import atomic
except ImportError:
    from django.db.transaction import commit_on_success as atomic


class AutoSingleRelatedObjectDescriptor(SingleRelatedObjectDescriptor):
    """
    The descriptor that handles the object creation for an AutoOneToOneField.
    """
    @atomic
    def __get__(self, instance, instance_type=None):
        model = getattr(self.related, 'related_model', self.related.model)

        try:
            return (super(AutoSingleRelatedObjectDescriptor, self)
                    .__get__(instance, instance_type))
        except model.DoesNotExist:
            # Using get_or_create instead() of save() or create() as it better handles race conditions
            model.objects.get_or_create(**{self.related.field.name: instance})

            # Don't return obj directly, otherwise it won't be added
            # to Django's cache, and the first 2 calls to obj.relobj
            # will return 2 different in-memory objects
            return (super(AutoSingleRelatedObjectDescriptor, self)
                    .__get__(instance, instance_type))


class AutoOneToOneField(OneToOneField):
    '''
    OneToOneField creates related object on first call if it doesnt exist yet.
    Use it instead of original OneToOne field.

    example:

        class MyProfile(models.Model):
            user = AutoOneToOneField(User, primary_key=True)
            home_page = models.URLField(max_length=255, blank=True)
            icq = models.IntegerField(max_length=255, null=True)
    '''
    def contribute_to_related_class(self, cls, related):
        setattr(cls, related.get_accessor_name(), AutoSingleRelatedObjectDescriptor(related))

if SOUTH:
    add_introspection_rules([
        (
            (AutoOneToOneField,),
            [],
            {
                "to": ["rel.to", {}],
                "to_field": ["rel.field_name", {"default_attr": "rel.to._meta.pk.name"}],
                "related_name": ["rel.related_name", {"default": None}],
                "db_index": ["db_index", {"default": True}],
            },
        )
        ],
        ["^annoying\.fields\.AutoOneToOneField"])


if VERSION >= (1, 8):
    JSONFieldBase = models.TextField
else:
    JSONFieldBase = six.with_metaclass(models.SubfieldBase, models.TextField)


class JSONField(JSONFieldBase):
    """
    JSONField is a generic textfield that neatly serializes/unserializes
    JSON objects seamlessly.
    Django snippet #1478

    example:
        class Page(models.Model):
            data = JSONField(blank=True, null=True)


        page = Page.objects.get(pk=5)
        page.data = {'title': 'test', 'type': 3}
        page.save()
    """

    def to_python(self, value):
        """
        Convert a string from the database to a Python value.
        """
        if value == "":
            return None

        try:
            if isinstance(value, basestring):
                return json.loads(value)
            elif isinstance(value, bytes):
                return json.loads(value.decode('utf8'))
        except ValueError:
            pass
        return value

    def get_prep_value(self, value):
        """
        Convert the value to a string so it can be stored in the database.
        """
        if value == "":
            return None
        if isinstance(value, dict) or isinstance(value, list):
            return json.dumps(value, cls=DjangoJSONEncoder, sort_keys=True, indent=2, separators=(',', ': '))
        return super(JSONField, self).get_prep_value(value)

    def from_db_value(self, value, *args, **kwargs):
        return self.to_python(value)

    def get_default(self):
        # Override Django's `get_default()` to avoid stringification.
        if self.has_default():
            if callable(self.default):
                return self.default()
            return self.default
        return ""

    def get_db_prep_save(self, value, *args, **kwargs):
        if value == "":
            return None
        if isinstance(value, dict) or isinstance(value, list):
            return json.dumps(value, cls=DjangoJSONEncoder, sort_keys=True, indent=2, separators=(',', ': '))
        else:
            return super(JSONField, self).get_db_prep_save(value, *args, **kwargs)

    def value_from_object(self, obj):
        value = super(JSONField, self).value_from_object(obj)
        if self.null and value is None:
            return None
        return json.dumps(value, sort_keys=True, indent=2, separators=(',', ': '))


if SOUTH:
    add_introspection_rules([], ["^annoying.fields.JSONField"])

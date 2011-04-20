from django.db import models

import uuid

class UUIDField(models.CharField):
    """
    A field which stores a UUID value in hex format. This may also have
    the Boolean attribute 'auto' which will set the value on initial save to a
    new UUID value (calculated using the UUID1 method). Note that while all
    UUIDs are expected to be unique we enforce this with a DB constraint.
    """
    # Modified from http://www.davidcramer.net/code/420/improved-uuidfield-in-django.html
    __metaclass__ = models.SubfieldBase

    def __init__(self, auto=False, *args, **kwargs):
#        if kwargs.get('primary_key', False):
#            assert auto, "Must pass auto=True when using UUIDField as primary key."
        self.auto = auto
        # Set this as a fixed value, we store UUIDs in text.
        kwargs['max_length'] = 32
        if auto:
            # Do not let the user edit UUIDs if they are auto-assigned.
            kwargs['editable'] = False
            kwargs['blank'] = True
            kwargs['unique'] = True
        super(UUIDField, self).__init__(*args, **kwargs)

    def db_type(self):
        return 'uuid'

    def pre_save(self, model_instance, add):
        """Ensures that we auto-set values if required. See CharField.pre_save."""
        value = getattr(model_instance, self.attname, None)
        if not value and self.auto:
            # Assign a new value for this attribute if required.
            value = uuid.uuid4().hex
            setattr(model_instance, self.attname, value)
        return value

    def to_python(self, value):
        if not value:
            return None
        return value

# from http://stackoverflow.com/questions/3459843/auto-truncating-fields-at-max-length-in-django-charfields
class TruncatingCharField(models.CharField):
    def get_prep_value(self, value):
        value = super(TruncatingCharField,self).get_prep_value(value)
        if value:
            return value[:self.max_length]
        return value


"""
UUID7 field implementation for Django models
"""
from django.db import models
from django.core.exceptions import ValidationError
from .uuid7 import uuid7, format_uuid7, uuid7_from_int, uuid7_from_str
import uuid

class UUID7Field(models.Field):
    """
    A field for storing UUID7 values in the database.
    """
    def __init__(self, storage_type='str', *args, **kwargs):
        """
        Initialize the field.
        
        Args:
            storage_type: Type to store in database ('str' or 'int')
        """
        if storage_type not in ('str', 'int'):
            raise ValueError("storage_type must be either 'str' or 'int'")
        self.storage_type = storage_type
        kwargs['default'] = kwargs.get('default', uuid7)
        super().__init__(*args, **kwargs)

    def get_internal_type(self):
        """
        Return the database column type.
        """
        if self.storage_type == 'int':
            return 'BigIntegerField'
        return 'CharField'

    def get_prep_value(self, value):
        """
        Convert the value to a format suitable for database storage.
        """
        if value is None:
            return None

        try:
            if isinstance(value, str):
                uuid_obj = uuid.UUID(value)
            elif isinstance(value, int):
                uuid_obj = uuid.UUID(int=value)
            elif isinstance(value, uuid.UUID):
                uuid_obj = value
            else:
                raise ValidationError(
                    f"Invalid UUID7 value type: {type(value)}. "
                    "Expected string, integer, or UUID object."
                )
            
            return format_uuid7(uuid_obj, self.storage_type)
        except ValueError as e:
            if isinstance(value, str):
                raise ValidationError(
                    f"Invalid UUID7 string format: '{value}'. "
                    "Expected format: 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'"
                )
            elif isinstance(value, int):
                raise ValidationError(
                    f"Invalid UUID7 integer value: {value}. "
                    "Value must be a valid 128-bit integer."
                )
            raise ValidationError(str(e))

    def to_python(self, value):
        """
        Convert the value to a Python UUID object.
        """
        if value is None:
            return None
        if isinstance(value, uuid.UUID):
            return value

        try:
            if self.storage_type == 'int':
                if not isinstance(value, int):
                    raise ValidationError(
                        f"Invalid UUID7 integer value: {value}. "
                        "Expected integer type."
                    )
                return uuid7_from_int(value)
            
            if not isinstance(value, str):
                raise ValidationError(
                    f"Invalid UUID7 string value: {value}. "
                    "Expected string type."
                )
            return uuid7_from_str(str(value))
        except ValueError as e:
            if self.storage_type == 'int':
                raise ValidationError(
                    f"Invalid UUID7 integer value: {value}. "
                    "Value must be a valid 128-bit integer."
                )
            raise ValidationError(
                f"Invalid UUID7 string format: '{value}'. "
                "Expected format: 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'"
            )

    def from_db_value(self, value, expression, connection):
        """
        Convert database value to Python value.
        """
        if value is None:
            return None

        try:
            if self.storage_type == 'int':
                if not isinstance(value, int):
                    raise ValidationError(
                        f"Invalid database value type: {type(value)}. "
                        "Expected integer for UUID7 integer storage."
                    )
                return uuid7_from_int(value)
            
            if not isinstance(value, str):
                raise ValidationError(
                    f"Invalid database value type: {type(value)}. "
                    "Expected string for UUID7 string storage."
                )
            return uuid7_from_str(str(value))
        except ValueError as e:
            if self.storage_type == 'int':
                raise ValidationError(
                    f"Invalid UUID7 integer value in database: {value}. "
                    "Value must be a valid 128-bit integer."
                )
            raise ValidationError(
                f"Invalid UUID7 string format in database: '{value}'. "
                "Expected format: 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'"
            )

    def formfield(self, **kwargs):
        """
        Return a form field for this model field.
        """
        from .forms import UUID7FormField
        defaults = {'form_class': UUID7FormField}
        defaults.update(kwargs)
        return super().formfield(**defaults) 
"""
UUID7 form field implementation for Django forms
"""
from django import forms
from django.core.exceptions import ValidationError
from .uuid7 import uuid7, format_uuid7, uuid7_from_int, uuid7_from_str
import uuid

class UUID7FormField(forms.Field):
    """
    A form field for UUID7 values.
    """
    def __init__(self, format_type='str', *args, **kwargs):
        """
        Initialize the field.
        
        Args:
            format_type: Type to output ('str' or 'int')
        """
        if format_type not in ('str', 'int'):
            raise ValueError("format_type must be either 'str' or 'int'")
        self.format_type = format_type
        kwargs['default'] = kwargs.get('default', uuid7)
        super().__init__(*args, **kwargs)

    def to_python(self, value):
        """
        Convert the input value to a UUID object.
        """
        if value is None:
            return None
        if isinstance(value, uuid.UUID):
            return value

        try:
            if isinstance(value, int):
                if self.format_type == 'str':
                    raise ValidationError(
                        "Integer value provided but field is configured for string format. "
                        "Please provide a UUID string in format: 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'"
                    )
                return uuid7_from_int(value)
            
            if isinstance(value, str):
                if self.format_type == 'int':
                    raise ValidationError(
                        "String value provided but field is configured for integer format. "
                        "Please provide a valid 128-bit integer."
                    )
                return uuid7_from_str(str(value))
            
            raise ValidationError(
                f"Invalid UUID7 value type: {type(value)}. "
                "Expected string or integer."
            )
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

    def prepare_value(self, value):
        """
        Convert the value to the specified format for form display.
        """
        if value is None:
            return None

        try:
            return format_uuid7(value, self.format_type)
        except ValueError as e:
            raise ValidationError(
                f"Failed to convert UUID7 to {self.format_type} format: {str(e)}"
            )

    def clean(self, value):
        """
        Clean and validate the value.
        """
        value = super().clean(value)
        if value is None and self.required:
            raise ValidationError(
                "This field is required."
            )
        return value 
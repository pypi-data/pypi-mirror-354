"""
UUID7 serializer field implementation for Django REST Framework
"""
from rest_framework import serializers
from .uuid7 import uuid7, format_uuid7, uuid7_from_int, uuid7_from_str
import uuid

class UUID7SerializerField(serializers.Field):
    """
    A serializer field for UUID7 values.
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

    def to_representation(self, value):
        """
        Convert the value to the specified format.
        """
        if value is None:
            return None

        try:
            return format_uuid7(value, self.format_type)
        except ValueError as e:
            raise serializers.ValidationError(
                f"Failed to convert UUID7 to {self.format_type} format: {str(e)}"
            )

    def to_internal_value(self, data):
        """
        Convert the input value to a UUID object.
        """
        if data is None:
            return None

        try:
            if isinstance(data, int):
                if self.format_type == 'str':
                    raise serializers.ValidationError(
                        "Integer value provided but field is configured for string format. "
                        "Please provide a UUID string in format: 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'"
                    )
                return uuid7_from_int(data)
            
            if isinstance(data, str):
                if self.format_type == 'int':
                    raise serializers.ValidationError(
                        "String value provided but field is configured for integer format. "
                        "Please provide a valid 128-bit integer."
                    )
                return uuid7_from_str(str(data))
            
            raise serializers.ValidationError(
                f"Invalid UUID7 value type: {type(data)}. "
                "Expected string or integer."
            )
        except ValueError as e:
            if isinstance(data, str):
                raise serializers.ValidationError(
                    f"Invalid UUID7 string format: '{data}'. "
                    "Expected format: 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'"
                )
            elif isinstance(data, int):
                raise serializers.ValidationError(
                    f"Invalid UUID7 integer value: {data}. "
                    "Value must be a valid 128-bit integer."
                )
            raise serializers.ValidationError(str(e)) 
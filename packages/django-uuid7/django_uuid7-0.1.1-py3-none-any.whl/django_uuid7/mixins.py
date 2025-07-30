"""
UUID7 mixins for Django models
"""
from .uuid7 import format_uuid7

class UUID7StringMixin:
    """
    Mixin to add string representation methods for UUID7 fields.
    """
    def get_uuid7_str(self, field_name: str) -> str:
        """
        Get string representation of a UUID7 field.
        
        Args:
            field_name: Name of the UUID7 field
            
        Returns:
            String representation of the UUID7
        """
        value = getattr(self, field_name)
        if value is None:
            return None
        return format_uuid7(value, 'str')
    
    def get_uuid7_int(self, field_name: str) -> int:
        """
        Get integer representation of a UUID7 field.
        
        Args:
            field_name: Name of the UUID7 field
            
        Returns:
            Integer representation of the UUID7
        """
        value = getattr(self, field_name)
        if value is None:
            return None
        return format_uuid7(value, 'int') 
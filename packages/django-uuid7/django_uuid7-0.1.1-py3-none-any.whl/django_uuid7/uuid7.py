"""
UUID7 implementation for Django
"""
import time
import uuid
import random
from typing import Optional, Union

def uuid7(timestamp: Optional[float] = None) -> uuid.UUID:
    """
    Generate a UUID7 (time-ordered UUID) based on the current timestamp.
    
    Args:
        timestamp: Optional timestamp to use instead of current time
        
    Returns:
        A UUID7 instance
    """
    if timestamp is None:
        timestamp = time.time()
    
    # Convert timestamp to milliseconds
    timestamp_ms = int(timestamp * 1000)
    
    # Get the current time in milliseconds
    current_ms = int(time.time() * 1000)
    
    # Generate random bytes for the remaining part
    random_bytes = random.getrandbits(80).to_bytes(10, 'big')
    
    # Construct the UUID7
    # First 48 bits: timestamp
    # Next 16 bits: sequence number (random)
    # Last 64 bits: random
    timestamp_bytes = timestamp_ms.to_bytes(6, 'big')
    sequence_bytes = random.getrandbits(16).to_bytes(2, 'big')
    
    # Combine all parts
    uuid_bytes = timestamp_bytes + sequence_bytes + random_bytes
    
    # Create UUID object
    return uuid.UUID(bytes=uuid_bytes)

def uuid7_to_int(uuid_obj: uuid.UUID) -> int:
    """
    Convert a UUID7 to an integer.
    
    Args:
        uuid_obj: UUID7 object to convert
        
    Returns:
        Integer representation of the UUID7
    """
    return int(uuid_obj.hex, 16)

def uuid7_to_str(uuid_obj: uuid.UUID) -> str:
    """
    Convert a UUID7 to a string.
    
    Args:
        uuid_obj: UUID7 object to convert
        
    Returns:
        String representation of the UUID7
    """
    return str(uuid_obj)

def uuid7_from_int(value: int) -> uuid.UUID:
    """
    Convert an integer to a UUID7.
    
    Args:
        value: Integer to convert
        
    Returns:
        UUID7 object
    """
    return uuid.UUID(int=value)

def uuid7_from_str(value: str) -> uuid.UUID:
    """
    Convert a string to a UUID7.
    
    Args:
        value: String to convert
        
    Returns:
        UUID7 object
    """
    return uuid.UUID(value)

def format_uuid7(value: Union[uuid.UUID, str, int], format_type: str = 'str') -> Union[str, int]:
    """
    Format a UUID7 value to the specified type.
    
    Args:
        value: UUID7 value (UUID object, string, or integer)
        format_type: Output format ('str' or 'int')
        
    Returns:
        Formatted UUID7 value
    """
    if isinstance(value, str):
        uuid_obj = uuid7_from_str(value)
    elif isinstance(value, int):
        uuid_obj = uuid7_from_int(value)
    elif isinstance(value, uuid.UUID):
        uuid_obj = value
    else:
        raise ValueError(f"Invalid UUID7 value type: {type(value)}")
    
    if format_type == 'int':
        return uuid7_to_int(uuid_obj)
    elif format_type == 'str':
        return uuid7_to_str(uuid_obj)
    else:
        raise ValueError(f"Invalid format type: {format_type}") 
"""Data validators"""
import re

def validate_mobile(mobile: str) -> bool:
    """Validate mobile number"""
    return bool(re.match(r'^[0-9]{10}$', mobile))

def validate_result_format(result: str) -> bool:
    """Validate result format"""
    # Format: XXX-XX-XXX or similar patterns
    return len(result) <= 20 and bool(re.match(r'^[0-9\-]*$', result))

def validate_username(username: str) -> bool:
    """Validate username"""
    return 3 <= len(username) <= 50 and bool(re.match(r'^[a-zA-Z0-9_]*$', username))

def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

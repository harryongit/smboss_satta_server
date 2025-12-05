"""Helper functions"""
from datetime import datetime, date

def get_today() -> date:
    """Get today's date"""
    return datetime.now().date()

def format_response(status: str, message: str, data: dict = None) -> dict:
    """Format API response"""
    response = {
        "status": status,
        "message": message,
        "timestamp": datetime.utcnow().isoformat()
    }
    
    if data:
        response.update(data)
    
    return response

def extract_jodi(result: str) -> str:
    """Extract jodi (middle 2 digits) from result"""
    # From "123-45-678" extract "45"
    parts = result.split('-')
    if len(parts) >= 2:
        return parts
    return None

def extract_panna(result: str, panna_type: str = "close") -> str:
    """Extract panna from result"""
    # From "123-45-678"
    # close_panna = "678" (last 3 digits)
    # open_panna = "123" (first 3 digits)
    parts = result.split('-')
    
    if panna_type == "close" and len(parts) >= 3:
        return parts
    elif panna_type == "open" and len(parts) >= 1:
        return parts
    
    return None

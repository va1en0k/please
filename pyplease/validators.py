

def validator(message, func=None):
    """Decorator for validators

    Usage: @validator('error message')"""
    def _decorator(func):
        func.error_message = message
        return func

    if func:
        return _decorator(func)
    
    return _decorator

# Default validators

@validator('Please enter a value')
def not_blank(value):
    return bool(value)

def variants(variants):
    """Validates that value is one of given"""
    
    variants = ', '.join(variants)
        
    @validator('Invalid value. Please select one of: %s' % variants)
    def _validator(value):
        return value.lower() in variants
    
    return _validator

import re
from rest_framework.exceptions import ValidationError


def validate_password(password):
    if len(password) < 8 or len(password) > 40:
        raise ValidationError("Password length must be 8–40 characters.")
    if not re.search(r'[A-Z]', password):
        raise ValidationError("Password must contain at least one Uppercase letter")
    if not re.search(r'[a-z]', password):
        raise ValidationError("Password must contain at least one lowercase letter.")
    if not re.search(r'\d', password):
        raise ValidationError("Password must contain at least one number.")
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        raise ValidationError("Password must contain at least one special character.")

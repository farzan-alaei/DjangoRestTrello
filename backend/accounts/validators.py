from django.core.exceptions import ValidationError


def validate_mobile(value):
    if not value.isdigit():
        raise ValidationError("Mobile number must be numeric")
    if len(value) != 11:
        raise ValidationError("Mobile number must be of 11 digits")
    return value

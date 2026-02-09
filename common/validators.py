from django.core.validators import RegexValidator

# Validators let you set custom conditions for model attributes

phone_number_validator = RegexValidator(
    regex = r'^\d{10}$',
    message = "Phone numbers must be exactly 10 digits long and not contain additional characters."
)
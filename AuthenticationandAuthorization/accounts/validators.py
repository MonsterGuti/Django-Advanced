from django.core.exceptions import ValidationError


class PracticalPasswordValidator:
    def validate(self, password):
        if len(set(password)) < 6:
            raise ValidationError('Password must contain at least 6 unique characters')

    def get_help_text(self):
        return 'Password must contain at least 6 unique characters'
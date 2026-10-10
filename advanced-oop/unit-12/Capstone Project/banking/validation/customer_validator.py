from __future__ import annotations
import re
from banking.exceptions import ValidationError


#Validate customer input before it reaches persistence or business logic
class CustomerValidator:
    #Validation rules for customer identity data

    EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
    USERNAME_PATTERN = re.compile(r"^[A-Za-z0-9_.-]{3,30}$")

    #Validate and normalise the supplied username value.
    def username(self, value: str) -> str:
        username = value.strip()

        if not self.USERNAME_PATTERN.fullmatch(username):
            raise ValidationError(
                "Username must be 3-30 characters and use only "
                "letters, numbers, '.', '_' or '-'."
            )

        return username

    #Validate and normalise the supplied email value
    def email(self, value: str) -> str:
        email = value.strip().lower()

        if not self.EMAIL_PATTERN.fullmatch(email):
            raise ValidationError("Invalid email address.")

        return email

    #Validate and normalise the supplied full name value.
    def full_name(self, value: str) -> str:
        full_name = value.strip()

        if len(full_name) < 2:
            raise ValidationError(
                "Full name must contain at least 2 characters."
            )

        return full_name

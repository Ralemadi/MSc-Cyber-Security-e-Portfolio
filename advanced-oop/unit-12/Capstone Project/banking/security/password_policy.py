from __future__ import annotations
import re
from dataclasses import dataclass
from banking.config import (
    PASSWORD_MAX_LENGTH,
    PASSWORD_MIN_LENGTH,
)


#Carry the structured password validation result returned by the service layer.
@dataclass(frozen=True)
class PasswordValidationResult:
    valid: bool
    errors: tuple[str, ...]


#Encapsulate the bank secure password rule independently from orchestration code.
class BankSecurePasswordPolicy:
    #Central password policy

    MIN_LENGTH = PASSWORD_MIN_LENGTH
    MAX_LENGTH = PASSWORD_MAX_LENGTH
    SPECIAL_PATTERN = re.compile(r"[^A-Za-z0-9]")

    #Evaluate the supplied value against this component's validation rules.
    def validate(
        self,
        password: str,
        username: str | None = None,
    ) -> PasswordValidationResult:
        errors: list[str] = []

        if not isinstance(password, str):
            return PasswordValidationResult(
                False,
                ("Password must be text.",),
            )

        if len(password) < self.MIN_LENGTH:
            errors.append(
                f"Password must be at least {self.MIN_LENGTH} characters."
            )

        if len(password) > self.MAX_LENGTH:
            errors.append(
                f"Password must not exceed {self.MAX_LENGTH} characters."
            )

        if not any(ch.isupper() for ch in password):
            errors.append("Password must contain an uppercase letter.")

        if not any(ch.islower() for ch in password):
            errors.append("Password must contain a lowercase letter.")

        if not self.SPECIAL_PATTERN.search(password):
            errors.append("Password must contain a special character.")

        if any(ch.isspace() for ch in password):
            errors.append("Password must not contain whitespace.")

        if username and username.lower() in password.lower():
            errors.append("Password must not contain the username.")

        return PasswordValidationResult(
            valid=not errors,
            errors=tuple(errors),
        )

    #Return a concise human-readable description of the active validation policy.
    def description(self) -> tuple[str, ...]:
        return (
            f"At least {self.MIN_LENGTH} characters",
            "At least one uppercase letter",
            "At least one lowercase letter",
            "At least one special character",
            "No whitespace",
            "Must not contain the username",
        )

from __future__ import annotations
from datetime import datetime

#Represent the controlled bank secure failure condition
class BankSecureError(Exception):
    #Base class for application-specific BankSecure errors
    pass


#Represent the controlled authentication failure condition
class AuthenticationError(BankSecureError):
    #Raised when authentication fails.
    pass


#Represent the controlled user disabled failure condition.
class UserDisabledError(AuthenticationError):
    #Raised when valid credentials belong to a disabled user
    pass


#Represent the controlled user temporarily locked failure condition.
class UserTemporarilyLockedError(AuthenticationError):
    #Raised while a five-minute failed-login lockout is active.

    #Initialise this component with its required dependencies and local state.
    def __init__(self, locked_until: datetime) -> None:
        self.locked_until = locked_until
        super().__init__(
            "This user account is temporarily locked until "
            f"{locked_until:%H:%M UTC}."
        )


#Represent the controlled authorization failure condition.
class AuthorizationError(PermissionError, BankSecureError):
    #Raised when an authenticated user is not allowed to perform an action.
    pass


#Represent the controlled validation failure condition.
class ValidationError(ValueError, BankSecureError):
    #Base application validation error.
    pass


#Represent the controlled invalid amount failure condition.
class InvalidAmountError(ValidationError):
    #Raised for invalid monetary input.
    pass


#Represent the controlled repository failure condition.
class RepositoryError(BankSecureError):
    #Base persistence-layer error.
    pass


#Represent the controlled duplicate username failure condition.
class DuplicateUsernameError(RepositoryError):
    #Raised when a username already exists.
    pass


#Represent the controlled duplicate email failure condition.
class DuplicateEmailError(RepositoryError):
    #Raised when an email address already exists.
    pass


#Represent the controlled account not found failure condition.
class AccountNotFoundError(RepositoryError):
    #Raised when a bank account cannot be found.
    pass


#Represent the controlled insufficient funds failure condition.
class InsufficientFundsError(RepositoryError):
    #Raised when an account does not have enough funds.
    pass


#Represent the controlled account status failure condition.
class AccountStatusError(BankSecureError):
   
    pass


#Represent the controlled transfer policy failure condition.
class TransferPolicyError(BankSecureError):
    #Raised when a banking/business transfer policy blocks a transfer
    pass


#Represent the controlled fraud rejected failure condition.
class FraudRejectedError(BankSecureError):
    #Public fraud rejection exception.


    #Initialise this component with its required dependencies and local state
    def __init__(
        self,
        risk_score: int,
        risk_reason: str,
    ) -> None:
        self.risk_score = risk_score
        self.risk_reason = risk_reason
        super().__init__(
            "Transfer rejected by security controls."
        )

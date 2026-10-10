from __future__ import annotations
from banking.domain.models import Customer
from banking.exceptions import AuthenticationError
from banking.services.customer_service import CustomerService


class SessionManager:
    #Own authenticated session state independently from the terminal UI.

    #Initialise this component with its required dependencies and local state
    def __init__(
        self,
        customer_service: CustomerService,
    ) -> None:
        self.customer_service = customer_service
        self._current_user: Customer | None = None

    #Expose the currently authenticated identity without modifying session state
    @property
    def current_user(self) -> Customer | None:
        return self._current_user

    #Report whether the current object satisfies the authenticated condition.
    @property
    def is_authenticated(self) -> bool:
        return self._current_user is not None

    #Authenticate credentials and establish the current session only after successful validation.
    def login(
        self,
        username: str,
        password: str,
    ) -> Customer:
        customer = self.customer_service.authenticate(
            username=username,
            password=password,
        )

        if customer is None:
            raise AuthenticationError(
                "Invalid username or password."
            )

        self._current_user = customer
        return customer

    #Clear the authenticated identity from the active session
    def logout(self) -> None:
        self._current_user = None

    #reload the authenticated identity so role and status changes are reflected in the active session
    def refresh_current_user(self) -> Customer | None:
        if self._current_user is None:
            return None

        refreshed = self.customer_service.get_customer(
            self._current_user.customer_id
        )

        if refreshed is None or not refreshed.enabled:
            self._current_user = None
            return None

        self._current_user = refreshed
        return refreshed

    #enforce the required user before returning control to the caller
    def require_user(self) -> Customer:
        if self._current_user is None:
            raise AuthenticationError(
                "Authentication is required."
            )

        return self._current_user

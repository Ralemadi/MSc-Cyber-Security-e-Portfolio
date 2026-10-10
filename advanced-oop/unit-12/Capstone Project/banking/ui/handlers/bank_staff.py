from __future__ import annotations
from banking.domain.account_identifier import format_account_id
from banking.security.privileges import Privilege
from banking.ui.handlers.base import BaseCommandHandler


class BankStaffCommandHandler(BaseCommandHandler):
    #BANK_STAFF customer/account creation workflows.

    def create_customer(self) -> None:
        staff = self.require_login()
        self.app.authorization_service.require_privilege(
            staff,
            Privilege.CREATE_CUSTOMER,
        )
        self.console.heading(
            "Create New Customer + First Account"
        )
        self.show_back_option()

        username = self._prompt_unique_username()
        full_name = self._prompt_full_name()
        email = self._prompt_unique_email()
        password = self.prompt_valid_password(
            username
        )
        account_type = self.prompt_account_type()
        opening_balance = self.prompt_opening_balance()

        result = (
            self.app.bank_staff_service
            .create_customer_with_account(
                actor=staff,
                username=username,
                full_name=full_name,
                email=email,
                password=password,
                account_type=account_type,
                opening_balance=opening_balance,
            )
        )

        self.console.success(
            f"Customer {result.customer.username} "
            "created successfully."
        )
        self.console.success(
            f"First account: "
            f"{format_account_id(result.account.account_id)}"
            f" | {result.account.account_type}"
            f" | Status: {result.account.status.value}"
            f" | Balance: {result.account.balance}"
        )

    def add_account_to_customer(self) -> None:
        staff = self.require_login()
        self.app.authorization_service.require_privilege(
            staff,
            Privilege.ADD_CUSTOMER_ACCOUNT,
        )
        self.console.heading(
            "Add Account to Existing Customer"
        )
        self.show_back_option()
        customer = self.select_customer_user(
            Privilege.ADD_CUSTOMER_ACCOUNT
        )
        account_type = self.prompt_account_type()
        opening_balance = self.prompt_opening_balance()

        result = self.app.bank_staff_service.add_account(
            actor=staff,
            customer=customer,
            account_type=account_type,
            opening_balance=opening_balance,
        )
        self.console.success(
            f"Account "
            f"{format_account_id(result.account.account_id)} "
            f"created for {result.customer.username}."
        )


    def _prompt_unique_username(self) -> str:
        while True:
            username = self.prompt_with_back(
                "Username"
            ).strip()

            try:
                username = (
                    self.app.customer_service
                    .validate_username(username)
                )
            except ValueError as exc:
                self.console.error(str(exc))
                continue

            if self.app.customer_service.username_exists(
                username
            ):
                self.console.error(
                    "This username already exists."
                )
                continue

            return username

    #Perform the internal prompt full name.
    def _prompt_full_name(self) -> str:
        while True:
            full_name = self.prompt_with_back(
                "Full name"
            ).strip()

            try:
                return self.app.customer_validator.full_name(
                    full_name
                )
            except ValueError as exc:
                self.console.error(str(exc))

    #Perform the internal prompt unique email .
    def _prompt_unique_email(self) -> str:
        while True:
            email = self.prompt_with_back(
                "Email"
            ).strip()

            try:
                email = (
                    self.app.customer_service
                    .validate_email(email)
                )
            except ValueError as exc:
                self.console.error(str(exc))
                continue

            if self.app.customer_service.email_exists(
                email
            ):
                self.console.error(
                    "This email already exists."
                )
                continue

            return email

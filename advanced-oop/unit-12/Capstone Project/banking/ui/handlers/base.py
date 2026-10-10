from __future__ import annotations
from banking.app.container import ApplicationContainer
from banking.domain.account_identifier import format_account_id
from banking.domain.models import Account, AccountStatus, Customer
from banking.security.privileges import Privilege
from banking.ui.console import Console
from banking.ui.navigation import ReturnToMainMenu


class BaseCommandHandler:
    #Shared terminal helpers used by focused command handlers.

    def __init__(
        self,
        app: ApplicationContainer,
        console: Console,
    ) -> None:
        self.app = app
        self.console = console

    #Enforce the required login before returning control to the caller.
    def require_login(self) -> Customer:
        return self.app.session_manager.require_user()

    #Display the reusable navigation option for returning to the main role menu.
    def show_back_option(self) -> None:
        self.console.warning("0. Back to Main Menu")

    #Prompt for and validate with back input before continuing.
    def prompt_with_back(
        self,
        label: str,
        *,
        secret: bool = False,
    ) -> str:
        prompt = f"{label} (0 to return): "
        value = (
            self.console.secret_prompt(prompt)
            if secret
            else self.console.prompt(prompt)
        )

        if value.strip() == "0":
            raise ReturnToMainMenu

        return value

    
    def account_label(
        self,
        account: Account,
        *,
        include_owner: bool,
        include_balance: bool = True,
    ) -> str:
        owner_text = ""
        balance_text = ""

        if include_owner:
            owner = self.app.customer_service.get_customer(
                account.customer_id
            )
            if owner is not None:
                owner_text = f" | Owner: {owner.username}"

        if include_balance:
            balance_text = f" | Balance: {account.balance}"

        return (
            f"{format_account_id(account.account_id)}"
            f" | {account.account_type}"
            f" | Status: {account.status.value}"
            f"{balance_text}"
            f"{owner_text}"
        )

    #List only authorised accounts and return the account selected by the user
    def select_accessible_account(
        self,
        title: str,
        privilege: Privilege,
        *,
        require_active: bool = False,
    ) -> Account:
        actor = self.require_login()

        while True:
            accounts = self.app.banking_service.accessible_accounts(
                actor,
                privilege,
            )

            if not accounts:
                raise ValueError(
                    "No accessible accounts are available."
                )

            self.console.normal(f"\n{title}")

            for index, account in enumerate(
                accounts,
                start=1,
            ):
                self.console.normal(
                    f"{index}. "
                    f"{self.account_label(account, include_owner=not actor.is_customer)}"
                )

            self.show_back_option()
            value = self.console.prompt(
                "Select account number: "
            ).strip()

            if value == "0":
                raise ReturnToMainMenu

            try:
                selected = int(value)
            except ValueError:
                self.console.error(
                    "Enter one of the displayed account numbers."
                )
                continue

            if not 1 <= selected <= len(accounts):
                self.console.error(
                    "Invalid account selection."
                )
                continue

            account = self.app.banking_service.get_accessible_account(
                actor,
                accounts[selected - 1].account_id,
                privilege,
            )

            if (
                require_active
                and account.status != AccountStatus.ACTIVE
            ):
                self.console.error(
                    f"{format_account_id(account.account_id)} "
                    f"is {account.status.value}. "
                    "Select an ACTIVE account."
                )
                continue

            return account

    #List eligible CUSTOMER identities and return the selected user.
    def select_customer_user(
        self,
        privilege: Privilege,
    ) -> Customer:
        actor = self.require_login()
        overviews = self.app.bank_staff_service.customer_overviews(
            actor,
            privilege,
        )
        customers = [
            overview.customer
            for overview in overviews
        ]

        if not customers:
            raise ValueError(
                "No CUSTOMER users are available."
            )

        while True:
            self.console.normal(
                "\nSelect customer:"
            )

            for index, customer in enumerate(
                customers,
                start=1,
            ):
                status = (
                    "ENABLED"
                    if customer.enabled
                    else "DISABLED"
                )
                self.console.normal(
                    f"{index}. {customer.username}"
                    f" | {customer.full_name}"
                    f" | {customer.email}"
                    f" | {status}"
                )

            self.show_back_option()
            value = self.console.prompt(
                "Customer number: "
            ).strip()

            if value == "0":
                raise ReturnToMainMenu

            try:
                selected = int(value)
            except ValueError:
                self.console.error(
                    "Enter a displayed customer number."
                )
                continue

            if not 1 <= selected <= len(customers):
                self.console.error(
                    "Invalid customer selection."
                )
                continue

            return customers[selected - 1]

    #Prompt for and validate account type input before continuing
    def prompt_account_type(self) -> str:
        mapping = {
            "1": "CURRENT",
            "2": "SAVINGS",
            "3": "SALARY",
        }

        while True:
            self.console.normal("\nAccount types:")
            self.console.normal("1. CURRENT")
            self.console.normal("2. SAVINGS")
            self.console.normal("3. SALARY")
            self.show_back_option()
            choice = self.console.prompt(
                "Select account type: "
            ).strip()

            if choice == "0":
                raise ReturnToMainMenu

            account_type = mapping.get(choice)

            if account_type is None:
                self.console.error(
                    "Invalid account type."
                )
                continue

            return account_type

    #Prompt for and validate opening balance input before continuing
    def prompt_opening_balance(self) -> str:
        while True:
            value = self.console.prompt(
                "Opening balance "
                "[press Enter for 0.00, 0 to return]: "
            ).strip()

            if value == "0":
                raise ReturnToMainMenu

            value = value or "0.00"

            try:
                self.app.account_service.opening_balance_to_money(
                    value
                )
            except ValueError as exc:
                self.console.error(str(exc))
                continue

            return value

    #Prompt for and validate valid password input before continuing
    def prompt_valid_password(
        self,
        username: str,
        label: str = "Password",
    ) -> str:
        self.console.warning("\nPassword Policy:")

        for rule in self.app.password_policy.description():
            self.console.warning(
                f" - {rule}"
            )

        while True:
            password = self.prompt_with_back(
                label,
                secret=True,
            )
            validation = self.app.password_policy.validate(
                password,
                username=username,
            )

            if not validation.valid:
                for error in validation.errors:
                    self.console.error(
                        f" - {error}"
                    )
                continue

            confirmation = self.prompt_with_back(
                "Confirm password",
                secret=True,
            )

            if password != confirmation:
                self.console.error(
                    "Passwords do not match."
                )
                continue

            return password

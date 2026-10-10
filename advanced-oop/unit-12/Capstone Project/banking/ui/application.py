from __future__ import annotations
from collections.abc import Callable
from banking.app.container import ApplicationContainer
from banking.domain.account_identifier import format_account_id
from banking.exceptions import (
    AuthenticationError,
    AuthorizationError,
    BankSecureError,
    UserDisabledError,
    UserTemporarilyLockedError,
)
from banking.security.privileges import Privilege
from banking.security.roles import UserRole
from banking.ui.console import Console
from banking.ui.handlers.account import AccountCommandHandler
from banking.ui.handlers.administrator import AdministratorCommandHandler
from banking.ui.handlers.bank_staff import BankStaffCommandHandler
from banking.ui.handlers.profile import ProfileCommandHandler
from banking.ui.handlers.transfer import TransferCommandHandler
from banking.ui.navigation import ReturnToMainMenu


class BankingCLI:

    #Initialise this component with its required dependencies and local state
    def __init__(
        self,
        app: ApplicationContainer,
        console: Console,
    ) -> None:
        self.app = app
        self.console = console
        self.account_handler = AccountCommandHandler(
            app,
            console,
        )
        self.bank_staff_handler = BankStaffCommandHandler(
            app,
            console,
        )
        self.administrator_handler = AdministratorCommandHandler(
            app,
            console,
        )
        self.profile_handler = ProfileCommandHandler(
            app,
            console,
        )
        self.transfer_handler = TransferCommandHandler(
            app,
            console,
        )

    #Run the interactive command loop until the user logs out or exits
    def run(self) -> None:
        while True:
            if not self.app.session_manager.is_authenticated:
                if not self._login_gate():
                    self.console.success(
                        "Thank you for using BankSecure. Goodbye."
                    )
                    return

            user = self.app.session_manager.require_user()

            if user.role == UserRole.CUSTOMER:
                keep_running = self._customer_menu()
            elif user.role == UserRole.BANK_STAFF:
                keep_running = self._bank_staff_menu()
            else:
                keep_running = self._administrator_menu()

            if not keep_running:
                return

    #Perform the internal login gate
    def _login_gate(self) -> bool:
        self.console.clear_screen()
        self.console.separator()
        self.console.bold("Welcome")
        self.console.normal(
            "to the BankSecure banking system interface."
        )
        self.console.separator()

        while True:
            username = self.console.prompt(
                "Username (0 to exit): "
            ).strip()

            if username == "0":
                return False

            password = self.console.secret_prompt(
                "Password: "
            )

            try:
                customer = self.app.session_manager.login(
                    username,
                    password,
                )
            except UserTemporarilyLockedError as exc:
                self.console.error(str(exc))
                continue
            except UserDisabledError as exc:
                self.console.error(str(exc))
                continue
            except AuthenticationError:
                self.console.error(
                    "Invalid username or password. Please try again."
                )
                continue

            self.console.success(
                f"Login successful. Welcome {customer.full_name}."
            )
            return True

    #Perform the internal customer menu
    def _customer_menu(self) -> bool:
        actions: dict[str, Callable[[], None]] = {
            "1": self.account_handler.view_accounts,
            "2": self.account_handler.view_balance,
            "3": self.account_handler.deposit,
            "4": self.account_handler.withdraw,
            "5": self.transfer_handler.transfer,
            "6": self.account_handler.transaction_history,
            "7": self.account_handler.summary_report,
            "8": self.profile_handler.change_password,
            "9": self._logout,
        }

        while self.app.session_manager.is_authenticated:
            self._show_authenticated_header()
            self.console.normal(
                "\n1. View My Account Details"
            )
            self.console.normal(
                "2. View My Account Balances"
            )
            self.console.normal(
                "3. Deposit Funds"
            )
            self.console.normal(
                "4. Withdraw Funds"
            )
            self.console.normal(
                "5. Transfer Funds"
            )
            self.console.normal(
                "6. View Transaction History"
            )
            self.console.normal(
                "7. Account Summary Report"
            )
            self.console.normal(
                "8. Change Password"
            )
            self.console.normal(
                "9. Logout"
            )
            self.console.normal(
                "0. Exit"
            )

            if not self._process_menu_choice(
                actions,
                maximum=9,
            ):
                return False

            if not self.app.session_manager.is_authenticated:
                return True

        return True

    #Perform the internal bank staff menu 
    def _bank_staff_menu(self) -> bool:
        actions: dict[str, Callable[[], None]] = {
            "1": self.bank_staff_handler.create_customer,
            "2": self.bank_staff_handler.add_account_to_customer,
            "3": self.account_handler.view_accounts,
            "4": self.account_handler.view_balance,
            "5": self.account_handler.deposit,
            "6": self.account_handler.withdraw,
            "7": self.transfer_handler.transfer,
            "8": self.account_handler.transaction_history,
            "9": self.account_handler.summary_report,
            "10": self.profile_handler.change_password,
            "11": self._logout,
        }

        while self.app.session_manager.is_authenticated:
            self._show_authenticated_header()
            self.console.normal(
                "\n1. Create New Customer + First Account"
            )
            self.console.normal(
                "2. Add Account to Existing Customer"
            )
            self.console.normal(
                "3. View Customers and Account Types"
            )
            self.console.normal(
                "4. View Customer Account Balances"
            )
            self.console.normal(
                "5. Deposit to Customer Account"
            )
            self.console.normal(
                "6. Withdraw from Customer Account"
            )
            self.console.normal(
                "7. Transfer Between Accounts"
            )
            self.console.normal(
                "8. View Account History"
            )
            self.console.normal(
                "9. Bank Summary Report"
            )
            self.console.normal(
                "10. Change Password"
            )
            self.console.normal(
                "11. Logout"
            )
            self.console.normal(
                "0. Exit"
            )

            if not self._process_menu_choice(
                actions,
                maximum=11,
            ):
                return False

            if not self.app.session_manager.is_authenticated:
                return True

        return True

    #Perform the internal administrator menu step
    def _administrator_menu(self) -> bool:
        actions: dict[str, Callable[[], None]] = {
            "1": self.administrator_handler.create_user,
            "2": self.administrator_handler.view_users,
            "3": self.administrator_handler.enable_user,
            "4": self.administrator_handler.disable_user,
            "5": self.administrator_handler.unlock_user,
            "6": self.administrator_handler.change_user_role,
            "7": self.administrator_handler.reset_user_password,
            "8": self.administrator_handler.administration_and_audit,
            "9": self.profile_handler.change_password,
            "10": self._logout,
        }

        while self.app.session_manager.is_authenticated:
            self._show_authenticated_header()
            self.console.normal(
                "\n1. Create User"
            )
            self.console.normal(
                "2. View Users"
            )
            self.console.normal(
                "3. Enable User"
            )
            self.console.normal(
                "4. Disable User"
            )
            self.console.normal(
                "5. Unlock Temporarily Locked User"
            )
            self.console.normal(
                "6. Assign / Change User Role"
            )
            self.console.normal(
                "7. Reset User Password"
            )
            self.console.normal(
                "8. Administration & Audit"
            )
            self.console.normal(
                "9. Change My Password"
            )
            self.console.normal(
                "10. Logout"
            )
            self.console.normal(
                "0. Exit"
            )

            if not self._process_menu_choice(
                actions,
                maximum=10,
            ):
                return False

            if not self.app.session_manager.is_authenticated:
                return True

        return True

    #Perform the internal process menu choice step
    def _process_menu_choice(
        self,
        actions: dict[str, Callable[[], None]],
        maximum: int,
    ) -> bool:
        choice = self.console.prompt(
            "\nSelect an option: "
        ).strip()

        if choice == "0":
            self.console.success(
                "Thank you for using BankSecure. Goodbye."
            )
            return False

        action = actions.get(choice)

        if action is None:
            self.console.error(
                f"Invalid option. Select 1-{maximum} or 0."
            )
            return True

        self._run_action(action)
        return True

    #Perform the internal run action step used by this workflow
    def _run_action(
        self,
        action: Callable[[], None],
    ) -> None:
        completed = False

        try:
            action()
            completed = True
        except ReturnToMainMenu:
            return
        except (
            AuthorizationError,
            PermissionError,
        ) as exc:
            self.console.error(
                f"ACCESS DENIED: {exc}"
            )
            completed = True
        except (
            BankSecureError,
            ValueError,
        ) as exc:
            self.console.error(str(exc))
            completed = True
        except Exception as exc:
    
            self.console.error(
                f"ERROR: {type(exc).__name__}: {exc}"
            )
            completed = True

        if (
            completed
            and action != self._logout
            and self.app.session_manager.is_authenticated
        ):
            self.console.back_to_main_menu()

    #Perform the internal show authenticated header
    def _show_authenticated_header(self) -> None:
        customer = self.app.session_manager.require_user()
        self.console.clear_screen()
        self.console.separator()
        self.console.bold("BankSecure")
        self.console.bold("Banking System")
        self.console.separator()

        line_one = (
            f"Logged in: {customer.username} |"
        )
        line_two = (
            f"{customer.full_name} | "
            f"Role: {customer.role.display_name}"
        )

        if customer.role == UserRole.ADMINISTRATOR:
            self.console.admin_info(line_one)
            self.console.admin_info(line_two)
        elif customer.role == UserRole.BANK_STAFF:
            self.console.staff_info(line_one)
            self.console.staff_info(line_two)
        else:
            self.console.user_info(line_one)
            self.console.user_info(line_two)

        self.console.separator()

        if customer.role == UserRole.CUSTOMER:
            self._print_home_accounts_compact()
            self.console.separator()

    def _print_home_accounts_compact(self) -> None:
        customer = self.app.session_manager.require_user()
        accounts = self.app.banking_service.accessible_accounts(
            customer,
            Privilege.VIEW_ACCOUNT_DETAILS,
        )
        self.console.user_info(
            "Your accounts:"
        )

        if not accounts:
            self.console.warning(
                "No accounts available."
            )
            return

        account_text = " | ".join(
            (
                f"{format_account_id(account.account_id)}/"
                f"{account.account_type}"
                f"[{account.status.value}]"
            )
            for account in accounts
        )
        self.console.user_info(
            account_text
        )

    #Perform the internal logout step used by this workflow
    def _logout(self) -> None:
        customer = self.app.session_manager.require_user()
        username = customer.username
        self.app.session_manager.logout()
        self.console.success(
            f"{username} logged out successfully."
        )

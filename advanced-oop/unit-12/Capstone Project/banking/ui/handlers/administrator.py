from __future__ import annotations
from banking.domain.account_identifier import format_account_id
from banking.domain.models import AccountStatus, Customer
from banking.security.privileges import Privilege
from banking.security.roles import UserRole
from banking.ui.handlers.base import BaseCommandHandler
from banking.ui.navigation import ReturnToMainMenu

class AdministratorCommandHandler(BaseCommandHandler):
    #ADMINISTRATOR identity, role, status, password and audit workflows

    #Create a system identity through the ADMINISTRATOR workflow
    def create_user(self) -> None:
        admin = self.require_login()
        self.app.authorization_service.require_privilege(
            admin,
            Privilege.CREATE_USER,
        )
        self.console.heading(
            "Create User"
        )
        self.show_back_option()

        username = self._prompt_unique_username()
        full_name = self._prompt_full_name()
        email = self._prompt_unique_email()
        role = self._prompt_role()
        password = self.prompt_valid_password(
            username
        )

        created = (
            self.app.user_admin_service
            .create_user(
                actor=admin,
                username=username,
                full_name=full_name,
                email=email,
                password=password,
                role=role,
            )
        )

        self.console.success(
            f"User {created.username} created successfully."
        )
        self.console.success(
            f"Role: {created.role.display_name}"
            f" | Status: ENABLED"
        )

    #Render system users with role, administrative status and temporary-lockout state
    def view_users(self) -> None:
        admin = self.require_login()
        self.console.heading(
            "View Users"
        )
        self.show_back_option()
        users = (
            self.app.user_admin_service
            .list_users(admin)
        )

        if not users:
            self.console.warning(
                "No users are available."
            )
            return

        self.console.normal(
            f"{'Username':<18} "
            f"{'Name':<24} "
            f"{'Role':<18} "
            f"{'Status':<36}"
        )
        self.console.normal(
            "-" * 102
        )

        for user in users:
            self.console.admin_info(
                f"{user.username:<18} "
                f"{user.full_name[:23]:<24} "
                f"{user.role.value:<18} "
                f"{user.status_description:<36}"
            )

    #Run the ADMINISTRATOR  that re-enables a selected user
    def enable_user(self) -> None:
        admin = self.require_login()
        self.console.heading(
            "Enable User"
        )
        self.show_back_option()
        target = self._select_user(
            admin,
            include_self=False,
        )
        updated = (
            self.app.user_admin_service
            .set_user_enabled(
                actor=admin,
                target=target,
                enabled=True,
            )
        )
        self.console.success(
            f"{updated.username} is now ENABLED."
        )

    #Run the ADMINISTRATOR  that disables a selected user
    def disable_user(self) -> None:
        admin = self.require_login()
        self.console.heading(
            "Disable User"
        )
        self.show_back_option()
        target = self._select_user(
            admin,
            include_self=False,
        )
        updated = (
            self.app.user_admin_service
            .set_user_enabled(
                actor=admin,
                target=target,
                enabled=False,
            )
        )
        self.console.success(
            f"{updated.username} is now DISABLED."
        )

    #Clear an active temporary login lockout through the ADMINISTRATOR-only 
    def unlock_user(self) -> None:
        admin = self.require_login()
        self.console.heading(
            "Unlock Temporarily Locked User"
        )
        self.show_back_option()
        target = self._select_user(
            admin,
            include_self=False,
            only_temporarily_locked=True,
        )
        updated = (
            self.app.user_admin_service
            .unlock_user(
                actor=admin,
                target=target,
            )
        )
        self.console.success(
            f"{updated.username} temporary login lockout has been cleared."
        )

    #Apply role-change restrictions before persisting the new system role
    def change_user_role(self) -> None:
        admin = self.require_login()
        self.console.heading(
            "Assign / Change User Role"
        )
        self.show_back_option()
        target = self._select_user(
            admin,
            include_self=False,
        )
        new_role = self._prompt_role()

        updated = (
            self.app.user_admin_service
            .change_user_role(
                actor=admin,
                target=target,
                role=new_role,
            )
        )
        self.console.success(
            f"{updated.username} role changed to "
            f"{updated.role.display_name}."
        )

    #Reset another users password through the ADMINISTRATOR-only workflow
    def reset_user_password(self) -> None:
        admin = self.require_login()
        self.console.heading(
            "Reset User Password"
        )
        self.show_back_option()
        target = self._select_user(
            admin,
            include_self=False,
        )
        new_password = self.prompt_valid_password(
            target.username,
            label="New password",
        )
        self.app.user_admin_service.reset_user_password(
            actor=admin,
            target=target,
            new_password=new_password,
        )
        self.console.success(
            f"Password reset successfully for "
            f"{target.username}."
        )

    #Display the ADMINISTRATOR submenu for audit review and account-status control
    def administration_and_audit(self) -> None:
        admin = self.require_login()

        while True:
            self.console.clear_screen()
            self.console.separator()
            self.console.bold(
                "Administration & Audit"
            )
            self.console.separator()
            self.console.normal(
                "1. View Audit Records"
            )
            self.console.normal(
                "2. Change Customer Account Status"
            )
            self.console.normal(
                "0. Back to Main Menu"
            )
            choice = self.console.prompt(
                "\nSelect an option: "
            ).strip()

            if choice == "0":
                return

            if choice == "1":
                self._view_audit_records()
            elif choice == "2":
                self._change_account_status()
            else:
                self.console.error(
                    "Invalid option."
                )
                continue

            self.console.back_to_main_menu()
            return

    #Perform the internal view audit records 
    def _view_audit_records(self) -> None:
        admin = self.require_login()
        self.console.heading(
            "Audit Records"
        )
        self.show_back_option()
        records = (
            self.app.user_admin_service
            .audit_records(
                admin,
                limit=30,
            )
        )

        if not records:
            self.console.warning(
                "No audit records are available."
            )
            return

        for record in records:
            risk = (
                f" | Risk={record.risk_score}"
                if record.risk_score is not None
                else ""
            )
            self.console.admin_info(
                f"{record.timestamp[:19]} "
                f"| {record.actor:<10} "
                f"| {record.action:<21} "
                f"| {record.outcome}{risk}"
            )

            if record.details:
                self.console.normal(
                    f"  Details: {record.details}"
                )

            if record.risk_reason:
                self.console.warning(
                    f"  Risk detail: {record.risk_reason}"
                )

    #Perform the internal change account status step 
    def _change_account_status(self) -> None:
        admin = self.require_login()
        self.console.heading(
            "Change Customer Account Status"
        )
        self.show_back_option()
        account = self.select_accessible_account(
            "Choose customer account:",
            Privilege.MANAGE_ACCOUNT_STATUS,
            require_active=False,
        )
        mapping = {
            "1": AccountStatus.ACTIVE,
            "2": AccountStatus.FROZEN,
            "3": AccountStatus.CLOSED,
        }

        while True:
            self.console.normal(
                "\n1. ACTIVE"
            )
            self.console.normal(
                "2. FROZEN"
            )
            self.console.normal(
                "3. CLOSED"
            )
            self.show_back_option()
            choice = self.console.prompt(
                "Select new status: "
            ).strip()

            if choice == "0":
                raise ReturnToMainMenu

            status = mapping.get(choice)

            if status is None:
                self.console.error(
                    "Invalid status selection."
                )
                continue

            updated = (
                self.app.user_admin_service
                .set_account_status(
                    actor=admin,
                    account_id=account.account_id,
                    status=status,
                )
            )
            self.console.success(
                f"{format_account_id(updated.account_id)} "
                f"status changed to {updated.status.value}."
            )
            return

    #Collect and validate the interactive selection for user
    def _select_user(
        self,
        admin: Customer,
        *,
        include_self: bool,
        only_temporarily_locked: bool = False,
    ) -> Customer:
        users = (
            self.app.user_admin_service
            .list_users(admin)
        )

        if not include_self:
            users = [
                user
                for user in users
                if user.customer_id != admin.customer_id
            ]

        if only_temporarily_locked:
            users = [
                user
                for user in users
                if user.is_temporarily_locked
            ]

        if not users:
            message = (
                "No temporarily locked users are available."
                if only_temporarily_locked
                else "No eligible users are available."
            )
            raise ValueError(message)

        while True:
            self.console.normal(
                "\nSelect user:"
            )

            for index, user in enumerate(
                users,
                start=1,
            ):
                self.console.normal(
                    f"{index}. {user.username}"
                    f" | {user.full_name}"
                    f" | {user.role.value}"
                    f" | {user.status_description}"
                )

            self.show_back_option()
            value = self.console.prompt(
                "User number: "
            ).strip()

            if value == "0":
                raise ReturnToMainMenu

            try:
                selected = int(value)
            except ValueError:
                self.console.error(
                    "Enter a displayed user number."
                )
                continue

            if not 1 <= selected <= len(users):
                self.console.error(
                    "Invalid user selection."
                )
                continue

            return users[selected - 1]

    #Perform the internal prompt role step
    def _prompt_role(self) -> UserRole:
        mapping = {
            "1": UserRole.CUSTOMER,
            "2": UserRole.BANK_STAFF,
            "3": UserRole.ADMINISTRATOR,
        }

        while True:
            self.console.normal(
                "\nRoles:"
            )
            self.console.normal(
                "1. CUSTOMER / CLIENT"
            )
            self.console.normal(
                "2. BANK STAFF"
            )
            self.console.normal(
                "3. ADMINISTRATOR"
            )
            self.show_back_option()
            value = self.console.prompt(
                "Select role: "
            ).strip()

            if value == "0":
                raise ReturnToMainMenu

            role = mapping.get(value)

            if role is None:
                self.console.error(
                    "Invalid role selection."
                )
                continue

            return role

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

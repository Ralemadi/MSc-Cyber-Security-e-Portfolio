from __future__ import annotations
from banking.domain.account_identifier import format_account_id
from banking.domain.transaction_identifier import format_transaction_id
from banking.exceptions import BankSecureError
from banking.patterns.visitors import PortfolioSummaryVisitor
from banking.security.privileges import Privilege
from banking.ui.handlers.base import BaseCommandHandler

class AccountCommandHandler(BaseCommandHandler):
    #Account views, balance changes, history and summary commands

    #Display the authorised accounts information through the CLI workflow
    def view_accounts(self) -> None:
        actor = self.require_login()
        self.console.heading(
            "Customers and Account Types"
            if actor.is_bank_staff
            else "My Account Details"
        )
        self.show_back_option()

        if actor.is_bank_staff:
            overviews = self.app.bank_staff_service.customer_overviews(
                actor,
                Privilege.VIEW_ACCOUNT_DETAILS,
            )

            if not overviews:
                self.console.warning(
                    "No customer profiles are available."
                )
                return

            for overview in overviews:
                profile = overview.customer
                status = (
                    "ENABLED"
                    if profile.enabled
                    else "DISABLED"
                )
                self.console.staff_info(
                    f"\nCustomer: {profile.username}"
                    f" | {profile.full_name}"
                    f" | {profile.email}"
                    f" | {status}"
                )

                if not overview.accounts:
                    self.console.warning(
                        "  No bank accounts."
                    )
                    continue

                for account in overview.accounts:
                    self.console.normal(
                        f"  {format_account_id(account.account_id)}"
                        f" | Type: {account.account_type}"
                        f" | Status: {account.status.value}"
                    )
            return

        accounts = self.app.banking_service.accessible_accounts(
            actor,
            Privilege.VIEW_ACCOUNT_DETAILS,
        )

        if not accounts:
            self.console.warning(
                "No accounts found."
            )
            return

        for account in accounts:
            self.console.user_info(
                self.account_label(
                    account,
                    include_owner=False,
                    include_balance=False,
                )
            )

    #Display the authorised balance information through the CLI workflow
    def view_balance(self) -> None:
        actor = self.require_login()
        self.console.heading(
            "Customer Account Balances"
            if actor.is_bank_staff
            else "My Account Balances"
        )
        self.show_back_option()
        accounts = self.app.banking_service.accessible_accounts(
            actor,
            Privilege.VIEW_ACCOUNT_BALANCES,
        )

        if not accounts:
            self.console.warning(
                "No accounts are available."
            )
            return

        for account in accounts:
            output = self.account_label(
                account,
                include_owner=actor.is_bank_staff,
                include_balance=True,
            )

            if actor.is_bank_staff:
                self.console.staff_info(output)
            else:
                self.console.user_info(output)

    #Validate authorization and account state before applying the deposit
    def deposit(self) -> None:
        actor = self.require_login()
        self.console.heading(
            "Deposit to Customer Account"
            if actor.is_bank_staff
            else "Deposit Funds"
        )
        self.show_back_option()
        account = self.select_accessible_account(
            "Choose account for deposit:",
            Privilege.DEPOSIT_FUNDS,
            require_active=True,
        )

        while True:
            amount = self.prompt_with_back(
                "Deposit amount"
            ).strip()

            try:
                result = self.app.banking_service.deposit(
                    actor=actor,
                    account_id=account.account_id,
                    amount=amount,
                )
                break
            except (ValueError, BankSecureError) as exc:
                self.console.error(
                    f"{exc} Please enter the amount again."
                )

        self.console.success(
            f"Deposit completed. "
            f"{format_account_id(result.account.account_id)} "
            f"new balance: {result.account.balance}"
        )

    #Validate authorization, account state and funds before applying the withdrawal
    def withdraw(self) -> None:
        actor = self.require_login()
        self.console.heading(
            "Withdraw from Customer Account"
            if actor.is_bank_staff
            else "Withdraw Funds"
        )
        self.show_back_option()
        account = self.select_accessible_account(
            "Choose account for withdrawal:",
            Privilege.WITHDRAW_FUNDS,
            require_active=True,
        )

        while True:
            amount = self.prompt_with_back(
                "Withdrawal amount"
            ).strip()

            try:
                result = self.app.banking_service.withdraw(
                    actor=actor,
                    account_id=account.account_id,
                    amount=amount,
                )
                break
            except (ValueError, BankSecureError) as exc:
                self.console.error(
                    f"{exc} Please enter the amount again."
                )

        self.console.success(
            f"Withdrawal completed. "
            f"{format_account_id(result.account.account_id)} "
            f"new balance: {result.account.balance}"
        )

    #Display authorised transaction history for the selected account
    def transaction_history(self) -> None:
        actor = self.require_login()
        self.console.heading(
            "Account History"
            if actor.is_bank_staff
            else "Transaction History"
        )
        self.show_back_option()
        account = self.select_accessible_account(
            "Choose account:",
            Privilege.VIEW_TRANSACTION_HISTORY,
            require_active=False,
        )
        transactions = self.app.banking_service.history(
            actor=actor,
            account_id=account.account_id,
        )

        if not transactions:
            self.console.warning(
                "No transactions found."
            )
            return

        self.console.normal(
            f"\nHistory for "
            f"{format_account_id(account.account_id)}"
        )
        self.console.normal("-" * 78)
        self.console.normal(
            f"{'Reference':<12} "
            f"{'Type':<16} "
            f"{'Amount':>10} "
            f"{'Status':<10} "
            f"{'Date':<10}"
        )
        self.console.normal("-" * 78)

        for tx in transactions:
            self.console.normal(
                f"{format_transaction_id(tx.transaction_id):<12} "
                f"{tx.transaction_type.value:<16} "
                f"{str(tx.amount):>10} "
                f"{tx.status.value:<10} "
                f"{tx.created_at.date().isoformat():<10}"
            )
            self.console.normal(
                f"  {tx.description}"
            )

    #Display the Visitor-based account or bank summary report
    def summary_report(self) -> None:
        actor = self.require_login()
        self.console.heading(
            "Bank Summary Report"
            if actor.is_bank_staff
            else "Account Summary Report"
        )
        self.show_back_option()
        visitor = PortfolioSummaryVisitor()
        accounts = self.app.banking_service.accessible_accounts(
            actor,
            Privilege.VIEW_ACCOUNT_SUMMARY,
        )

        if not accounts:
            self.console.warning(
                "No accounts available."
            )
            return

        visited_transactions: set[int] = set()

        for account in accounts:
            account.accept(visitor)

            for tx in self.app.account_service.history(
                account.account_id
            ):
                if tx.transaction_id in visited_transactions:
                    continue

                tx.accept(visitor)
                visited_transactions.add(
                    tx.transaction_id
                )

        result = visitor.result()
        self.console.success(
            f"Accounts: {result['account_count']}"
        )
        self.console.success(
            f"Total balance: {result['total_balance']}"
        )
        self.console.success(
            f"Transactions reviewed: "
            f"{result['transaction_count']}"
        )
        self.console.success(
            f"Transaction types: "
            f"{result['transaction_types']}"
        )

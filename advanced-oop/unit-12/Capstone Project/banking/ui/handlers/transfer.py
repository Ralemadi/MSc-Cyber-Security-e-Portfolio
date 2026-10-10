from __future__ import annotations
from banking.domain.account_identifier import parse_account_id
from banking.domain.models import Account, AccountStatus
from banking.exceptions import (
    AccountStatusError,
    BankSecureError,
    FraudRejectedError,
    InsufficientFundsError,
    TransferPolicyError,
)
from banking.security.privileges import Privilege
from banking.ui.handlers.base import BaseCommandHandler
from banking.ui.navigation import ReturnToMainMenu


#Coordinate deposit, withdrawal and transfer input/output.
class TransferCommandHandler(BaseCommandHandler):

    #execute the coordinated transfer workflow through policy, fraud, persistence and notification controls.
    def transfer(self) -> None:
        actor = self.require_login()
        self.console.heading(
            "Transfer Between Accounts"
            if actor.is_bank_staff
            else "Transfer Funds"
        )
        self.show_back_option()
        source = self.select_accessible_account(
            "Choose source account:",
            Privilege.TRANSFER_FUNDS,
            require_active=True,
        )
        destination = self._select_destination_account(
            source
        )

        while True:
            amount = self.prompt_with_back(
                "Transfer amount"
            ).strip()

            try:
                result = self.app.banking_service.transfer(
                    actor=actor,
                    from_account_id=source.account_id,
                    to_account_id=destination.account_id,
                    amount=amount,
                )
                break
            except FraudRejectedError as exc:
                # Provider score/reason stays internal and is written to audit
                self.console.error(str(exc))
                self.console.warning(
                    "Please enter a different amount."
                )
            except (
                TransferPolicyError,
                InsufficientFundsError,
                AccountStatusError,
                ValueError,
            ) as exc:
                self.console.error(str(exc))
                self.console.warning(
                    "Please enter a different amount."
                )

        self.console.success(
            "Transfer completed successfully."
        )
        self.console.success(
            result.customer_message
        )

    #Collect and validate the interactive selection for destination account
    def _select_destination_account(
        self,
        source: Account,
    ) -> Account:
        actor = self.require_login()

        if actor.is_bank_staff:
            return self._select_staff_destination(
                source
            )

        return self._select_customer_destination(
            source
        )

    #Collect and validate the interactive selection for staff destination
    def _select_staff_destination(
        self,
        source: Account,
    ) -> Account:
        while True:
            actor = self.require_login()
            accounts = [
                item
                for item
                in self.app.banking_service.accessible_accounts(
                    actor,
                    Privilege.TRANSFER_FUNDS,
                )
                if item.account_id != source.account_id
            ]
            self.console.normal(
                "\nSelect destination:"
            )

            for index, account in enumerate(
                accounts,
                start=1,
            ):
                self.console.normal(
                    f"{index}. "
                    f"{self.account_label(account, include_owner=True)}"
                )

            self.show_back_option()
            value = self.console.prompt(
                "Destination number: "
            ).strip()

            if value == "0":
                raise ReturnToMainMenu

            try:
                selected = int(value)
            except ValueError:
                self.console.error(
                    "Enter a valid destination number."
                )
                continue

            if not 1 <= selected <= len(accounts):
                self.console.error(
                    "Invalid destination selection."
                )
                continue

            destination = accounts[selected - 1]

            if destination.status != AccountStatus.ACTIVE:
                self.console.error(
                    "Destination account must be ACTIVE."
                )
                continue

            return destination

    #Collect and validate the interactive selection for customer destination
    def _select_customer_destination(
        self,
        source: Account,
    ) -> Account:
        while True:
            self.show_back_option()
            value = self.console.prompt(
                "Recipient Account ID "
                "(e.g. QTR00000005): "
            ).strip()

            if value == "0":
                raise ReturnToMainMenu

            try:
                destination = self.app.account_service.get_account(
                    parse_account_id(value)
                )
            except (
                ValueError,
                TypeError,
                BankSecureError,
            ) as exc:
                self.console.error(str(exc))
                continue

            if destination.account_id == source.account_id:
                self.console.error(
                    "Source and destination must be different."
                )
                continue

            if destination.status != AccountStatus.ACTIVE:
                self.console.error(
                    "Destination account is not ACTIVE."
                )
                continue

            owner = self.app.customer_service.get_customer(
                destination.customer_id
            )

            if owner is None or not owner.is_customer:
                self.console.error(
                    "Recipient must be a CUSTOMER bank account."
                )
                continue

            return destination

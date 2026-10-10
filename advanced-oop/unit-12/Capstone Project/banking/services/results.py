from __future__ import annotations
from dataclasses import dataclass
from banking.domain.models import Account, Customer
from banking.domain.money import Money


#Carry the structured deposit result returned by the service layer
@dataclass(frozen=True)
class DepositResult:
    account: Account
    amount: Money


#Carry the structured withdrawal result returned by the service layer
@dataclass(frozen=True)
class WithdrawalResult:
    account: Account
    amount: Money


#Carry the structured account creation result returned by the service layer
@dataclass(frozen=True)
class AccountCreationResult:
    customer: Customer
    account: Account

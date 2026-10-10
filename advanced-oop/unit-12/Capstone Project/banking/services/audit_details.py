from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Protocol, runtime_checkable



@runtime_checkable
class AuditDetails(Protocol):
   
    def to_dict(self) -> dict[str, Any]:
        ...



@dataclass(frozen=True)
class TransferAuditDetails:
    from_account: str
    to_account: str
    amount: str
    transaction_reference: str | None = None
    error_type: str | None = None


    def to_dict(self) -> dict[str, Any]:
        return {
            key: value
            for key, value in asdict(self).items()
            if value is not None
        }



@dataclass(frozen=True)
class BalanceChangeAuditDetails:
    account: str
    amount: str
    error_type: str | None = None


    def to_dict(self) -> dict[str, Any]:
        return {
            key: value
            for key, value in asdict(self).items()
            if value is not None
        }



@dataclass(frozen=True)
class CustomerAuditDetails:
    customer: str
    account: str
    account_type: str

 
    def to_dict(self) -> dict[str, Any]:
        return asdict(self)



@dataclass(frozen=True)
class AccountStatusAuditDetails:
    account: str
    new_status: str


    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


#Carry structured user audit details for the audit trail.
@dataclass(frozen=True)
class UserAuditDetails:
    username: str
    role: str
    enabled: bool


    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


#Carry structured user status audit details for the audit trail.
@dataclass(frozen=True)
class UserStatusAuditDetails:
    username: str
    enabled: bool

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


#Carry structured role change audit details for the audit trail.
@dataclass(frozen=True)
class RoleChangeAuditDetails:
    username: str
    old_role: str
    new_role: str


    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


#Carry structured password audit details for the audit trail.
@dataclass(frozen=True)
class PasswordAuditDetails:
    username: str
    mode: str


    def to_dict(self) -> dict[str, Any]:
        return asdict(self)



#Carry structured login security audit details for the audit trail.
@dataclass(frozen=True)
class LoginSecurityAuditDetails:
    username: str
    failed_attempts: int | None = None
    locked_until: str | None = None


    def to_dict(self) -> dict[str, Any]:
        return {
            key: value
            for key, value in asdict(self).items()
            if value is not None
        }

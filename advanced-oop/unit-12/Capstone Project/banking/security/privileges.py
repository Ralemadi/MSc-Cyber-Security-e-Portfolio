from __future__ import annotations
from enum import Enum
from banking.security.roles import UserRole



#Enumerate individual actions that can be granted through role-based access control
class Privilege(str, Enum):
    #Individual permissions. Privileges are independent from role names.

    VIEW_ACCOUNT_DETAILS = "VIEW_ACCOUNT_DETAILS"
    VIEW_ACCOUNT_BALANCES = "VIEW_ACCOUNT_BALANCES"
    DEPOSIT_FUNDS = "DEPOSIT_FUNDS"
    WITHDRAW_FUNDS = "WITHDRAW_FUNDS"
    TRANSFER_FUNDS = "TRANSFER_FUNDS"
    VIEW_TRANSACTION_HISTORY = "VIEW_TRANSACTION_HISTORY"
    VIEW_ACCOUNT_SUMMARY = "VIEW_ACCOUNT_SUMMARY"
    CHANGE_OWN_PASSWORD = "CHANGE_OWN_PASSWORD"

    CREATE_CUSTOMER = "CREATE_CUSTOMER"
    ADD_CUSTOMER_ACCOUNT = "ADD_CUSTOMER_ACCOUNT"

    CREATE_USER = "CREATE_USER"
    VIEW_USERS = "VIEW_USERS"
    ENABLE_USER = "ENABLE_USER"
    DISABLE_USER = "DISABLE_USER"
    UNLOCK_USER = "UNLOCK_USER"
    ASSIGN_USER_ROLE = "ASSIGN_USER_ROLE"
    RESET_USER_PASSWORD = "RESET_USER_PASSWORD"
    VIEW_AUDIT = "VIEW_AUDIT"
    MANAGE_ACCOUNT_STATUS = "MANAGE_ACCOUNT_STATUS"


ROLE_PRIVILEGES: dict[UserRole, frozenset[Privilege]] = {
    UserRole.CUSTOMER: frozenset(
        {
            Privilege.VIEW_ACCOUNT_DETAILS,
            Privilege.VIEW_ACCOUNT_BALANCES,
            Privilege.DEPOSIT_FUNDS,
            Privilege.WITHDRAW_FUNDS,
            Privilege.TRANSFER_FUNDS,
            Privilege.VIEW_TRANSACTION_HISTORY,
            Privilege.VIEW_ACCOUNT_SUMMARY,
            Privilege.CHANGE_OWN_PASSWORD,
        }
    ),
    UserRole.BANK_STAFF: frozenset(
        {
            Privilege.CREATE_CUSTOMER,
            Privilege.ADD_CUSTOMER_ACCOUNT,
            Privilege.VIEW_ACCOUNT_DETAILS,
            Privilege.VIEW_ACCOUNT_BALANCES,
            Privilege.DEPOSIT_FUNDS,
            Privilege.WITHDRAW_FUNDS,
            Privilege.TRANSFER_FUNDS,
            Privilege.VIEW_TRANSACTION_HISTORY,
            Privilege.VIEW_ACCOUNT_SUMMARY,
            Privilege.CHANGE_OWN_PASSWORD,
        }
    ),
    UserRole.ADMINISTRATOR: frozenset(
        {
            Privilege.CREATE_USER,
            Privilege.VIEW_USERS,
            Privilege.ENABLE_USER,
            Privilege.DISABLE_USER,
            Privilege.UNLOCK_USER,
            Privilege.ASSIGN_USER_ROLE,
            Privilege.RESET_USER_PASSWORD,
            Privilege.VIEW_AUDIT,
            Privilege.MANAGE_ACCOUNT_STATUS,
            Privilege.CHANGE_OWN_PASSWORD,
        }
    ),
}


#Return the immutable privilege set assigned to the requested role
def privileges_for(role: UserRole) -> frozenset[Privilege]:
    #Return the immutable privilege set assigned to a role
    return ROLE_PRIVILEGES.get(role, frozenset())

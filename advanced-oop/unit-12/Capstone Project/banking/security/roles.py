from __future__ import annotations
from enum import Enum


#Enumerate the CUSTOMER, BANK_STAFF and ADMINISTRATOR business roles
class UserRole(str, Enum):
    #Application roles. Roles identify the users business function

    CUSTOMER = "CUSTOMER"
    BANK_STAFF = "BANK_STAFF"
    ADMINISTRATOR = "ADMINISTRATOR"

    #Expose the user-friendly role label used by the terminal presentation layer
    @property
    def display_name(self) -> str:
        labels = {
            UserRole.CUSTOMER: "CUSTOMER / CLIENT",
            UserRole.BANK_STAFF: "BANK STAFF",
            UserRole.ADMINISTRATOR: "ADMINISTRATOR",
        }
        return labels[self]

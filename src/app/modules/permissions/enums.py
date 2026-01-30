from enum import Enum


class RoleEnum(str, Enum):
    OWNER = "owner"
    ADMIN = "admin"
    ACCOUNTANT = "accountant"
    CLIENT = "client"
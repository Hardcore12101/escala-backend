from enum import Enum


class RoleEnum(str, Enum):
    ADMIN = "admin"
    ACCOUNTANT = "accountant"
    CLIENT = "client"

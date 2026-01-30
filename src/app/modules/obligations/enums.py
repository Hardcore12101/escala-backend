from enum import Enum


class ObligationType(str, Enum):
    DAS = "das"
    IRPJ = "irpj"
    CSLL = "csll"
    ICMS = "icms"
    ISS = "iss"


class ObligationStatus(str, Enum):
    PENDING = "pending"
    PAID = "paid"
    OVERDUE = "overdue"

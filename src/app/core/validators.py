import re

def validate_cnpj(cnpj: str) -> bool:
    cnpj = re.sub(r"\D", "", cnpj)
    return len(cnpj) == 14

from dataclasses import dataclass
from src.app.modules.users.models import User
from src.app.models.company import Company
from src.app.modules.permissions.enums import RoleEnum


@dataclass
class CurrentContext:
    user: User
    company: Company
    role: RoleEnum

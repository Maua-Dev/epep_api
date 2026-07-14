from enum import Enum

class RoleEnum(str, Enum):
    ADMIN = "admin"
    USER = "user"
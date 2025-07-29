from enum import Enum


class V0042AssocSharesObjWrapTypeItem(str, Enum):
    ASSOCIATION = "ASSOCIATION"
    USER = "USER"

    def __str__(self) -> str:
        return str(self.value)

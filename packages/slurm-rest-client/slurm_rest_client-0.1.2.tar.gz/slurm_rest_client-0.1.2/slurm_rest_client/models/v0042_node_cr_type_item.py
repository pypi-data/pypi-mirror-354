from enum import Enum


class V0042NodeCrTypeItem(str, Enum):
    AVAILABLE = "AVAILABLE"
    ONE_ROW = "ONE_ROW"
    RESERVED = "RESERVED"

    def __str__(self) -> str:
        return str(self.value)

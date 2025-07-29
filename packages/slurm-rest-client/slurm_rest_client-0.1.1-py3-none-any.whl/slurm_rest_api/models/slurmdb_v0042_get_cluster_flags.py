from enum import Enum


class SlurmdbV0042GetClusterFlags(str, Enum):
    EXTERNAL = "EXTERNAL"
    FEDERATION = "FEDERATION"
    FRONT_END = "FRONT_END"
    MULTIPLE_SLURMD = "MULTIPLE_SLURMD"
    REGISTERING = "REGISTERING"

    def __str__(self) -> str:
        return str(self.value)

from dataclasses import dataclass


@dataclass
class Design:
    datatype: str
    operation: str
    width: int
    part: str
    period: int

    def __str__(self):
        return (
            f"{self.datatype}_{self.operation}_{self.width}_{self.part}_{self.period}"
        )


__all__ = ["Design"]

# src/core/domain/shared/money.py
from dataclasses import dataclass

@dataclass(frozen=True)
class Money:
    currency: str
    amount: float
    def __post_init__(self):
        if self.amount < 0:
            raise ValueError("amount must be >= 0")
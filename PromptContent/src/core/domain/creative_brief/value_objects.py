from dataclasses import dataclass

@dataclass(frozen=True)
class Budget:
    currency: str
    amount: float
    def __post_init__(self):
        if self.amount < 0:
            raise ValueError("budget must be >= 0")
        object.__setattr__(self, "currency", self.currency.upper())

@dataclass(frozen=True)
class Audience:
    persona: str
    country: str   # ISO-3166-1 alpha-2
    language: str  # BCP-47
    interests: list[str] | None = None

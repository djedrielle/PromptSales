# src/core/domain/campaign_planning/entities.py
from dataclasses import dataclass, field
from enum import Enum
from typing import List
from src.core.domain.shared.money import Money
from src.core.domain.shared.time_range import DateRange

class CampaignStatus(str, Enum):
    draft = "draft"
    scheduled = "scheduled"
    active = "active"
    paused = "paused"

@dataclass
class KPI:
    metric: str
    target_value: float

@dataclass
class Campaign:
    id: str | None
    name: str
    period: DateRange
    budget: Money
    status: CampaignStatus = CampaignStatus.draft
    kpis: List[KPI] = field(default_factory=list)

    @classmethod
    def create(cls, name: str, period: DateRange, budget: Money) -> "Campaign":
        return cls(id=None, name=name, period=period, budget=budget, status=CampaignStatus.draft)

    def set_kpis(self, kpis: List[KPI]) -> None:
        self.kpis = kpis

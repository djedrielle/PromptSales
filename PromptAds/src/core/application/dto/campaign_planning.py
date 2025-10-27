# src/core/application/dto/campaign_planning.py
from dataclasses import dataclass
from datetime import date

@dataclass
class CreateCampaignCmd:
    name: str
    start: date
    end: date
    currency: str
    budget_amount: float

@dataclass
class DefineKpisCmd:
    campaign_id: str
    kpis: list[dict]  # [{"metric": "ctr", "target_value": 2.5}, ...]

@dataclass
class CampaignReadDto:
    id: str
    name: str
    status: str
    start: date
    end: date
    budget_amount: float
    currency: str
    kpis: list[dict]

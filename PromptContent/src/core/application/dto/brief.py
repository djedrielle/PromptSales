from dataclasses import dataclass
from datetime import date
from typing import List, Dict

@dataclass
class CreateBriefCmd:
    title: str
    objective: str
    channels: List[str]
    deadline: date
    budget_currency: str
    budget_amount: float
    audiences: List[Dict]           # [{persona,country,language,interests?}]
    brand_guidelines: str | None = None
    forbidden_topics: List[str] | None = None
    legal_notes: str | None = None

@dataclass
class BriefReadDto:
    id: str
    title: str
    status: str
    deadline: date
    budget_amount: float
    budget_currency: str
    channels: List[str]
    audiences: List[Dict]

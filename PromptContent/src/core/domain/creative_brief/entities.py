from dataclasses import dataclass, field
from enum import Enum
from datetime import date, datetime
from typing import List
from .value_objects import Budget, Audience

class BriefStatus(str, Enum):
    draft = "draft"

@dataclass
class Brief:
    id: str | None
    title: str
    objective: str
    channels: List[str]
    deadline: date
    budget: Budget
    audiences: List[Audience]
    brand_guidelines: str = ""
    forbidden_topics: List[str] = field(default_factory=list)
    legal_notes: str = ""
    status: BriefStatus = BriefStatus.draft
    created_at: datetime = field(default_factory=datetime.utcnow)

    @classmethod
    def create(cls, title, objective, channels, deadline, budget, audiences,
               brand_guidelines, forbidden_topics, legal_notes, created_at):
        if not channels:
            raise ValueError("at least one channel required")
        return cls(
            id=None, title=title, objective=objective, channels=channels,
            deadline=deadline, budget=budget, audiences=audiences,
            brand_guidelines=brand_guidelines, forbidden_topics=forbidden_topics,
            legal_notes=legal_notes, status=BriefStatus.draft, created_at=created_at
        )

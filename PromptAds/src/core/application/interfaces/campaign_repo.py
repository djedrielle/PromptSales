# src/core/application/interfaces/campaign_repo.py
from typing import Protocol, Optional
from src.core.domain.campaign_planning.entities import Campaign

class ICampaignRepository(Protocol):
    def save(self, c: Campaign) -> Campaign: ...
    def by_id(self, cid: str) -> Optional[Campaign]: ...

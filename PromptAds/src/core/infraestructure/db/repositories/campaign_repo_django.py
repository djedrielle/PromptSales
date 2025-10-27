# src/core/infrastructure/db/repositories/campaign_repo_django.py
from src.core.application.interfaces.campaign_repo import ICampaignRepository
from src.core.domain.campaign_planning.entities import Campaign, KPI, CampaignStatus
from src.core.domain.shared.money import Money
from src.core.domain.shared.time_range import DateRange
from ..models.campaign import CampaignModel

def to_entity(m: CampaignModel) -> Campaign:
    return Campaign(
        id=m.id,
        name=m.name,
        status=CampaignStatus(m.status),
        period=DateRange(m.start, m.end),
        budget=Money(m.currency, float(m.budget_amount)),
        kpis=[],
    )

class CampaignRepositoryDjango(ICampaignRepository):
    def save(self, c: Campaign) -> Campaign:
        m, _ = CampaignModel.objects.update_or_create(
            id=c.id or None,
            defaults=dict(
                name=c.name,
                status=c.status.value,
                start=c.period.start,
                end=c.period.end,
                budget_amount=c.budget.amount,
                currency=c.budget.currency,
            ),
        )
        return to_entity(m)

    def by_id(self, cid: str) -> Campaign | None:
        m = CampaignModel.objects.filter(id=cid).first()
        return to_entity(m) if m else None

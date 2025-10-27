# src/core/application/use_cases/campaign_planning/create_campaign.py
from src.core.application.dto.campaign_planning import CreateCampaignCmd, CampaignReadDto
from src.core.application.interfaces.campaign_repo import ICampaignRepository
from src.core.application.interfaces.unit_of_work import IUnitOfWork
from src.core.domain.campaign_planning.entities import Campaign
from src.core.domain.shared.money import Money
from src.core.domain.shared.time_range import DateRange

class CreateCampaign:
    def __init__(self, repo: ICampaignRepository, uow: IUnitOfWork):
        self.repo = repo
        self.uow = uow

    def __call__(self, cmd: CreateCampaignCmd) -> CampaignReadDto:
        c = Campaign.create(
            name=cmd.name,
            period=DateRange(cmd.start, cmd.end),
            budget=Money(cmd.currency, cmd.budget_amount),
        )
        with self.uow:
            saved = self.repo.save(c)
            self.uow.commit()
        return CampaignReadDto(
            id=saved.id or "",
            name=saved.name,
            status=saved.status.value,
            start=saved.period.start,
            end=saved.period.end,
            budget_amount=saved.budget.amount,
            currency=saved.budget.currency,
            kpis=[{"metric": k.metric, "target_value": k.target_value} for k in saved.kpis],
        )

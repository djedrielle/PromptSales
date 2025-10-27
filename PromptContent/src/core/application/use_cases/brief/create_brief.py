from datetime import datetime
from src.core.application.dto.brief import CreateBriefCmd, BriefReadDto
from src.core.application.interfaces.brief_repo import IBriefRepository
from src.core.application.interfaces.unit_of_work import IUnitOfWork
from src.core.domain.creative_brief.entities import Brief
from src.core.domain.creative_brief.value_objects import Budget, Audience

class CreateBrief:
    def __init__(self, repo: IBriefRepository, uow: IUnitOfWork):
        self.repo, self.uow = repo, uow

    def __call__(self, cmd: CreateBriefCmd) -> BriefReadDto:
        audiences = [
            Audience(a["persona"], a["country"], a["language"], a.get("interests") or [])
            for a in cmd.audiences
        ]
        b = Brief.create(
            title=cmd.title,
            objective=cmd.objective,
            channels=cmd.channels,
            deadline=cmd.deadline,
            budget=Budget(cmd.budget_currency.upper(), cmd.budget_amount),
            audiences=audiences,
            brand_guidelines=cmd.brand_guidelines or "",
            forbidden_topics=cmd.forbidden_topics or [],
            legal_notes=cmd.legal_notes or "",
            created_at=datetime.utcnow(),
        )
        with self.uow:
            saved = self.repo.create(b)
            self.uow.commit()
        return BriefReadDto(
            id=saved.id or "",
            title=saved.title,
            status=saved.status.value,
            deadline=saved.deadline,
            budget_amount=saved.budget.amount,
            budget_currency=saved.budget.currency,
            channels=saved.channels,
            audiences=[a.__dict__ for a in saved.audiences],
        )

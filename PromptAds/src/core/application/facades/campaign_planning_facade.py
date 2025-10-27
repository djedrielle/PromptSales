# src/core/application/facades/campaign_planning_facade.py
from src.core.application.dto.campaign_planning import CreateCampaignCmd, DefineKpisCmd, CampaignReadDto
from src.core.application.interfaces.campaign_repo import ICampaignRepository
from src.core.application.interfaces.unit_of_work import IUnitOfWork
from src.core.application.use_cases.campaign_planning.create_campaign import CreateCampaign
from src.core.application.use_cases.campaign_planning.define_kpis import DefineKpis  # crea este similar

class CampaignPlanningFacade:
    def __init__(self, repo: ICampaignRepository, uow: IUnitOfWork):
        self._create = CreateCampaign(repo, uow)
        self._define = DefineKpis(repo, uow)

    def create_campaign(self, cmd: CreateCampaignCmd) -> CampaignReadDto:
        return self._create(cmd)

    def define_kpis(self, cmd: DefineKpisCmd) -> CampaignReadDto:
        return self._define(cmd)

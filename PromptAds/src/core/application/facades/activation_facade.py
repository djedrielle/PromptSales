# src/core/application/facades/activation_facade.py
from src.core.application.dto.activation import ActivateCmd, ActivationReadDto  # define dto
from src.core.application.interfaces.campaign_repo import ICampaignRepository
from src.core.application.interfaces.ads_router import IAdsProviderRouter
from src.core.application.interfaces.unit_of_work import IUnitOfWork
from src.core.application.use_cases.activation.activate_campaign import ActivateCampaign

class ActivationFacade:
    def __init__(self, repo: ICampaignRepository, ads: IAdsProviderRouter, uow: IUnitOfWork):
        self._activate = ActivateCampaign(repo, ads, uow)

    def activate(self, cmd: ActivateCmd) -> ActivationReadDto:
        return self._activate(cmd)

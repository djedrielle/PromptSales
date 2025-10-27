# src/api/v1/campaign/views.py
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from .serializers import CreateCampaignSerializer
from .permissions import CanManageCampaigns
from src.core.application.dto.campaign_planning import CreateCampaignCmd
from src.core.application.facades.campaign_planning_facade import CampaignPlanningFacade
from src.core.infrastructure.db.repositories.campaign_repo_django import CampaignRepositoryDjango
from src.core.infrastructure.db.unit_of_work_django import DjangoUnitOfWork

class CampaignViewSet(ViewSet):
    permission_classes = [CanManageCampaigns]

    def create(self, request):
        s = CreateCampaignSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        cmd = CreateCampaignCmd(**s.validated_data)

        facade = CampaignPlanningFacade(
            repo=CampaignRepositoryDjango(),
            uow=DjangoUnitOfWork()
        )
        dto = facade.create_campaign(cmd)
        return Response(dto.__dict__, status=status.HTTP_201_CREATED)

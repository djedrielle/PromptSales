from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status

from .serializers import CreateBriefSerializer
from src.core.application.dto.brief import CreateBriefCmd, BriefReadDto
from src.core.application.facades.brief_facade import BriefFacade
from src.core.infrastructure.db.mongo.client import get_collection
from src.core.infrastructure.db.mongo.brief_repo_mongo import BriefRepositoryMongo
from src.core.application.interfaces.unit_of_work import IUnitOfWork

class NoopUoW(IUnitOfWork):
    def __enter__(self): return self
    def __exit__(self, *args): return False
    def commit(self): pass
    def rollback(self): pass

def facade_factory() -> BriefFacade:
    repo = BriefRepositoryMongo(get_collection())
    return BriefFacade(repo=repo, uow=NoopUoW())

class BriefViewSet(ViewSet):
    def create(self, request):
        s = CreateBriefSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        cmd = CreateBriefCmd(**s.validated_data)
        dto: BriefReadDto = facade_factory().create_brief(cmd)
        return Response(dto.__dict__, status=status.HTTP_201_CREATED)

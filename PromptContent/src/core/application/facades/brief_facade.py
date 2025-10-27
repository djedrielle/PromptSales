from src.core.application.dto.brief import CreateBriefCmd, BriefReadDto
from src.core.application.interfaces.brief_repo import IBriefRepository
from src.core.application.interfaces.unit_of_work import IUnitOfWork
from src.core.application.use_cases.brief.create_brief import CreateBrief

class BriefFacade:
    def __init__(self, repo: IBriefRepository, uow: IUnitOfWork):
        self._create = CreateBrief(repo, uow)

    def create_brief(self, cmd: CreateBriefCmd) -> BriefReadDto:
        return self._create(cmd)

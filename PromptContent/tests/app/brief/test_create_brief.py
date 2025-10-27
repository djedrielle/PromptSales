from datetime import date
from src.core.application.dto.brief import CreateBriefCmd
from src.core.application.facades.brief_facade import BriefFacade

class FakeRepo:
    def create(self, b): b.id = "brf_1"; return b
    def by_id(self, bid): return None

class NoopUoW:
    def __enter__(self): return self
    def __exit__(self, *a): pass
    def commit(self): pass
    def rollback(self): pass

def test_create_brief_ok():
    facade = BriefFacade(FakeRepo(), NoopUoW())
    cmd = CreateBriefCmd(
        title="Lanzamiento X",
        objective="Awareness",
        channels=["facebook","instagram"],
        deadline=date(2025,1,31),
        budget_currency="usd",
        budget_amount=1500,
        audiences=[{"persona":"GenZ","country":"CR","language":"es-CR"}]
    )
    dto = facade.create_brief(cmd)
    assert dto.id == "brf_1"
    assert dto.status == "draft"
    assert dto.channels == ["facebook","instagram"]

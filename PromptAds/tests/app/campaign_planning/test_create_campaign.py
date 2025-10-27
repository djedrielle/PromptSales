# tests/app/campaign_planning/test_create_campaign.py
from datetime import date
from src.core.application.dto.campaign_planning import CreateCampaignCmd
from src.core.application.facades.campaign_planning_facade import CampaignPlanningFacade

class FakeRepo:
    def save(self, c): 
        c.id = "cmp_1"; 
        return c
    def by_id(self, cid): 
        return None

class FakeUoW:
    def __enter__(self): return self
    def __exit__(self, *args): pass
    def commit(self): pass

def test_create_campaign_ok():
    facade = CampaignPlanningFacade(FakeRepo(), FakeUoW())
    cmd = CreateCampaignCmd(name="Brand X", start=date(2025,1,1), end=date(2025,2,1), currency="USD", budget_amount=1000)
    dto = facade.create_campaign(cmd)
    assert dto.id == "cmp_1"
    assert dto.status == "draft"

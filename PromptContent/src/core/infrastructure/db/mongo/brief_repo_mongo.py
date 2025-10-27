from typing import Optional
from bson import ObjectId
from pymongo.collection import Collection
from datetime import datetime

from src.core.application.interfaces.brief_repo import IBriefRepository
from src.core.domain.creative_brief.entities import Brief, BriefStatus
from src.core.domain.creative_brief.value_objects import Budget, Audience

def _to_doc(b: Brief) -> dict:
    return {
        "_id": ObjectId(),
        "title": b.title,
        "objective": b.objective,
        "channels": b.channels,
        "deadline": b.deadline,
        "budget": {"currency": b.budget.currency, "amount": b.budget.amount},
        "audiences": [a.__dict__ for a in b.audiences],
        "brand_guidelines": b.brand_guidelines,
        "forbidden_topics": b.forbidden_topics,
        "legal_notes": b.legal_notes,
        "status": b.status.value,
        "created_at": b.created_at or datetime.utcnow(),
    }

def _to_entity(d: dict) -> Brief:
    budget = Budget(d["budget"]["currency"], float(d["budget"]["amount"]))
    audiences = [Audience(a["persona"], a["country"], a["language"], a.get("interests") or []) for a in d.get("audiences", [])]
    return Brief(
        id=str(d["_id"]),
        title=d["title"],
        objective=d["objective"],
        channels=d["channels"],
        deadline=d["deadline"],
        budget=budget,
        audiences=audiences,
        brand_guidelines=d.get("brand_guidelines", ""),
        forbidden_topics=d.get("forbidden_topics", []),
        legal_notes=d.get("legal_notes", ""),
        status=BriefStatus(d.get("status","draft")),
        created_at=d.get("created_at") or datetime.utcnow()
    )

class BriefRepositoryMongo(IBriefRepository):
    def __init__(self, col: Collection):
        self.col = col

    def create(self, b: Brief) -> Brief:
        doc = _to_doc(b)
        self.col.insert_one(doc)
        b.id = str(doc["_id"])
        return b

    def by_id(self, bid: str) -> Optional[Brief]:
        d = self.col.find_one({"_id": ObjectId(bid)})
        return _to_entity(d) if d else None

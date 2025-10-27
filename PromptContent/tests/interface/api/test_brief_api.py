from django.urls import reverse
from rest_framework.test import APIClient

def test_create_brief_endpoint(db):
    client = APIClient()
    client.force_authenticate(user=type("U",(object,),{"is_authenticated":True,"scopes":["briefs:write"]})())
    url = reverse("briefs-list")
    res = client.post(url, {
        "title":"Campaña Summer",
        "objective":"Leads para promos",
        "channels":["facebook","tiktok"],
        "deadline":"2025-01-31",
        "budget_currency":"USD",
        "budget_amount":5000,
        "audiences":[{"persona":"GenZ","country":"CR","language":"es-CR"}]
    }, format="json")
    assert res.status_code == 201
    assert res.data["title"] == "Campaña Summer"

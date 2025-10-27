# tests/interface/api/test_campaign_api.py
from django.urls import reverse
from rest_framework.test import APIClient

def test_create_campaign_endpoint(db):
    client = APIClient()
    # simula auth simple
    client.force_authenticate(user=type("U",(object,),{"is_authenticated":True,"scopes":["campaigns:write"]})())
    url = reverse("campaigns-list")
    res = client.post(url, {
        "name": "Brand Y",
        "start": "2025-01-01",
        "end": "2025-02-01",
        "currency": "USD",
        "budget_amount": 500
    }, format="json")
    assert res.status_code == 201
    assert res.data["name"] == "Brand Y"

# src/core/infrastructure/external/ads/google_adapter.py
import httpx
from src.core.application.interfaces.ads_provider import IAdsProvider

class GoogleAdsAdapter(IAdsProvider):
    def __init__(self, base_url: str, token: str, timeout: int = 10):
        self.client = httpx.Client(base_url=base_url, timeout=timeout, headers={"Authorization": f"Bearer {token}"})
    def publish(self, payload: dict) -> dict:
        r = self.client.post("/adsets", json=payload)
        r.raise_for_status()
        return r.json()
    def pause(self, external_id: str) -> None:
        r = self.client.post(f"/adsets/{external_id}/pause"); r.raise_for_status()
    def status(self, external_id: str) -> dict:
        r = self.client.get(f"/adsets/{external_id}"); r.raise_for_status(); return r.json()

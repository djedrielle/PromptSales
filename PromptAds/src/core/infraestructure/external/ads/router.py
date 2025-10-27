# src/core/infrastructure/external/ads/router.py
from src.core.application.interfaces.ads_router import IAdsProviderRouter
from src.core.application.interfaces.ads_provider import IAdsProvider
from .google_adapter import GoogleAdsAdapter
from .meta_adapter import MetaAdsAdapter
from .tiktok_adapter import TikTokAdsAdapter

class AdsProviderRouter(IAdsProviderRouter):
    def __init__(self, google: GoogleAdsAdapter, meta: MetaAdsAdapter, tiktok: TikTokAdsAdapter):
        self._map = {"google": google, "meta": meta, "tiktok": tiktok}
    def for_channel(self, channel: str) -> IAdsProvider:
        return self._map[channel]

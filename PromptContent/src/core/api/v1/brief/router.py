from rest_framework.routers import DefaultRouter
from .views import BriefViewSet

router = DefaultRouter()
router.register(r"briefs", BriefViewSet, basename="briefs")
urlpatterns = router.urls

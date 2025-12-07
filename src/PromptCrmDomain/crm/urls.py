from django.urls import path
from . import views

urlpatterns = [
    path('api/health', views.health_check, name='health_check'),
    path('api/lead-metrics', views.lead_metrics_api, name='lead_metrics'),
]

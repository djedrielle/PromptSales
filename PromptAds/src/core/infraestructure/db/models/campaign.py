# src/core/infrastructure/db/models/campaign.py
from django.db import models

class CampaignModel(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    name = models.CharField(max_length=180)
    status = models.CharField(max_length=24, default="draft")
    start = models.DateField()
    end = models.DateField()
    budget_amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=6, default="USD")
    created_at = models.DateTimeField(auto_now_add=True)

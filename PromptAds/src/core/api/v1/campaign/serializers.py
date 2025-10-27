# src/api/v1/campaign/serializers.py
from rest_framework import serializers

class CreateCampaignSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=180)
    start = serializers.DateField()
    end = serializers.DateField()
    currency = serializers.CharField(max_length=6)
    budget_amount = serializers.FloatField(min_value=0)

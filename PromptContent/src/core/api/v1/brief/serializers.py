from rest_framework import serializers

class AudienceSerializer(serializers.Serializer):
    persona = serializers.CharField(max_length=120)
    country = serializers.CharField(max_length=2)      # ISO-3166-1 alpha-2
    language = serializers.CharField(max_length=10)    # p.ej. es-CR
    interests = serializers.ListField(
        child=serializers.CharField(max_length=60), required=False
    )

class CreateBriefSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=180)
    objective = serializers.CharField(max_length=2000)
    channels = serializers.ListField(
        child=serializers.ChoiceField(
            choices=["facebook","instagram","tiktok","youtube","search","display","email"]
        ),
        min_length=1,
    )
    deadline = serializers.DateField()
    budget_currency = serializers.CharField(max_length=6)
    budget_amount = serializers.FloatField(min_value=0)
    audiences = AudienceSerializer(many=True, min_length=1)
    brand_guidelines = serializers.CharField(required=False, allow_blank=True)
    forbidden_topics = serializers.ListField(
        child=serializers.CharField(max_length=80), required=False
    )
    legal_notes = serializers.CharField(required=False, allow_blank=True)

    def validate_budget_currency(self, v: str):
        v = v.upper()
        if len(v) not in (3, 4, 5, 6):
            raise serializers.ValidationError("currency must be 3–6 chars")
        return v

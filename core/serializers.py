from rest_framework import serializers
from core.models import Client, Policy


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = "__all__"


class PolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = Policy
        fields = [
            "policy_id",
            "policy_number",
            "branch",
            "start_date",
            "end_date",
            "status",
            "premium_amount",
        ]

from rest_framework import serializers
from urlshortner.models import UrlData

class UrlDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = UrlData
        fields = ["origin_url", "hash", "expire_at"]
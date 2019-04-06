from rest_framework import serializers
from . import models


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id',
            'price',
            'discounted',
        )
        model = models.Item

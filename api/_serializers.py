from rest_framework import serializers
from . import models


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'

        model = models.Item


class VoucherSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'

        model = models.Voucher


class BasketSerializer(serializers.ModelSerializer):
    class Meta:
        # fields = '__all__'
        fields = (
            'items',
        )

        model = models.Basket


class TrolleySerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'

        model = models.Trolley


class OrderHistorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'

        model = models.OrderHistory

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


class VoucherSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'code',
            'discounted_rate',
        )
        model = models.Voucher


class BasketSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'user',
            'items',
        )
        model = models.Basket


class TrolleySerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'user',
            'items',
            'total_price',
        )
        model = models.Trolley


class OrderHistorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'user',
            'date',
            'items',
            'total_paid',
            'payment_method',
        )
        model = models.OrderHistory

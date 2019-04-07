from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault
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
        fields = (
            'items',
        )

        model = models.Basket

    def validate(self, data):
        user = self.context['request'].user
        if models.Basket.objects.filter(user=user).exists():
            error_message = 'Sorry you can\'t add basket, visit basket/change to add more items'
            raise serializers.ValidationError(error_message)
        else:
            for item in data['items']:
                if item not in models.Item.objects.all().values_list('id', flat=True):
                    raise serializers.ValidationError("You enter invalid item ID")
        return data


class TrolleySerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'

        model = models.Trolley


class OrderHistorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'

        model = models.OrderHistory

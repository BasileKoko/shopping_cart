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
        request = self.context['request']
        if request.method == 'POST':
            if models.Basket.objects.filter(user=request.user).exists():
                error_message = 'Sorry you cannot add basket, visit basket/change to add more items'
                raise serializers.ValidationError(error_message)

        for item in data['items']:
            if item not in models.Item.objects.all().values_list('id', flat=True):
                error_message = 'You add invalid item ID'
                raise serializers.ValidationError(error_message)

        return data


class TrolleySerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'

        model = models.Trolley


class OrderHistorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'

        model = models.OrderHistory

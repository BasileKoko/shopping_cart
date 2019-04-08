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
        fields = (
            'items',
        )

        model = models.Basket

    def validate(self, data):
        request = self.context['request']
        if request.method == 'POST':
            if models.Basket.objects.filter(user=request.user).exists():
                error_message = 'Basket is created, you cannot create a second one. Visit /change to add more items'
                raise serializers.ValidationError(error_message)

        for item in data['items']:
            if item not in models.Item.objects.all().values_list('id', flat=True):
                error_message = 'You add invalid item ID'
                raise serializers.ValidationError(error_message)

        return data


class TrolleySerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'items',
            'total_price',
        )

        model = models.Trolley
        readonly_only_fields = ('user', 'total_price')

    def validate(self, data):
        request = self.context['request']
        if request.method == 'POST':
            if models.Trolley.objects.filter(user=request.user).exists():
                error_message = 'Trolley is created, you cannot create a second one. Visit /change to add items'
                raise serializers.ValidationError(error_message)

        for item in data['items']:
            if item not in models.Item.objects.all().values_list('id', flat=True):
                error_message = 'You add invalid item ID'
                raise serializers.ValidationError(error_message)

        return data


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        read_only_fields = ('user', 'items', 'total_paid', 'status')

        model = models.Order

    def validate(self, data):
        request = self.context['request']
        if request.method == 'POST':
            if not models.Trolley.objects.filter(user=request.user).exclude(items=[]).exists():
                error_message = 'You can place an order for empty trolley empty, add items first'
                raise serializers.ValidationError(error_message)
        return data

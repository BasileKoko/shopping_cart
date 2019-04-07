from django.db import IntegrityError
from rest_framework import generics
from rest_framework.response import Response

from api.utils import remove_item_from_basket_update_or_create_trolley, calculate_trolley_total_price
from . import _serializers
from . import models


class ItemView(generics.ListAPIView):

    queryset = models.Item.objects.all()
    serializer_class = _serializers.ItemSerializer


class ItemDetailView(generics.RetrieveAPIView):

    queryset = models.Item.objects.all()
    serializer_class = _serializers.ItemSerializer


class BasketAddListView(generics.ListCreateAPIView):

    serializer_class = _serializers.BasketSerializer

    def get_queryset(self):
        queryset = models.Basket.objects.filter(user=self.request.user)

        return queryset

    def perform_create(self, serializer):
        user = self.request.user
        serializer.validated_data['user'] = user
        serializer.save(user=user)

        return super(BasketAddListView, self).create(serializer)


class BasketChangeView(generics.RetrieveUpdateAPIView):
    serializer_class = _serializers.BasketSerializer
    queryset = models.Basket.objects.all()


class BasketAddItemToTrolleyView(generics.RetrieveUpdateAPIView):
    serializer_class = _serializers.BasketSerializer
    queryset = models.Basket.objects.all()

    def perform_update(self, serializer):
        user = self.request.user
        updated_item_ids = serializer.validated_data['items']
        remove_item_from_basket_update_or_create_trolley(user, updated_item_ids)
        serializer.save(user=user)

        return super(BasketAddItemToTrolleyView, self).perform_update(serializer)


class TrolleyAddListView(generics.ListCreateAPIView):
    serializer_class = _serializers.TrolleySerializer

    def get_queryset(self):
        queryset = models.Trolley.objects.filter(user=self.request.user)

        return queryset

    def perform_create(self, serializer):
        user = self.request.user
        serializer.validated_data['user'] = user
        item_ids = serializer.validated_data['items']
        total_price = calculate_trolley_total_price(item_ids)
        serializer.save(user=user, total_price=total_price)

        return super(TrolleyAddListView, self).create(serializer)

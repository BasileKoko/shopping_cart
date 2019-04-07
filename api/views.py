from django.db import IntegrityError
from rest_framework import generics
from rest_framework.response import Response

from api.utils import remove_item_from_basket_update_or_create_trolley
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
    # queryset = models.Trolley.objects.all()

    def get_queryset(self):
        queryset = models.Trolley.objects.filter(user=self.request.user)

        return queryset

    def perform_create(self, serializer):
        user = self.request.user
        serializer.validated_data['user'] = user
        serializer.save(user=user)

        return super(TrolleyAddListView, self).create(serializer)

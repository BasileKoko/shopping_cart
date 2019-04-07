from django.db import IntegrityError
from rest_framework import generics
from rest_framework.response import Response

from . import _serializers
from . import models


class ItemView(generics.ListAPIView):

    queryset = models.Item.objects.all()
    serializer_class = _serializers.ItemSerializer


class ItemDetailView(generics.RetrieveAPIView):

    queryset = models.Item.objects.all()
    serializer_class = _serializers.ItemSerializer


class BasketAddView(generics.ListCreateAPIView):

    serializer_class = _serializers.BasketSerializer

    def get_queryset(self):
        queryset = models.Basket.objects.filter(user=self.request.user)

        return queryset

    def perform_create(self, serializer):
        user = self.request.user
        serializer.validated_data['user'] = user
        serializer.save(user=user)

        return super(BasketAddView, self).create(serializer)


class BasketChangeView(generics.RetrieveUpdateAPIView):
    serializer_class = _serializers.BasketSerializer
    queryset = models.Basket.objects.all()

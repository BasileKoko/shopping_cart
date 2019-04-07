from rest_framework import generics, serializers
from . import _serializers
from . import models


class ItemView(generics.ListAPIView):

    queryset = models.Item.objects.all()
    serializer_class = _serializers.ItemSerializer


class ItemDetailView(generics.RetrieveAPIView):

    queryset = models.Item.objects.all()
    serializer_class = _serializers.ItemSerializer


class BasketView(generics.ListCreateAPIView):

    queryset = models.Basket.objects.all()
    serializer_class = _serializers.BasketSerializer

    def perform_create(self, serializer):
        serializer.validated_data['user'] = self.request.user.id
        serializer.save(user=self.request.user)

        return super(BasketView, self).create(serializer)

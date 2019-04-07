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
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )
    # user = serializers.PrimaryKeyRelatedField(
    #     read_only=True,
    #     default=serializers.CurrentUserDefault()
    # )

    # def perform_create(self, serializer):

        # serializer.save(user=user)



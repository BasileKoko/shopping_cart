from rest_framework import generics
from . import serializers
from . import models


class ItemView(generics.ListAPIView):
    authentication_classes = []
    permission_classes = []

    queryset = models.Item.objects.all()
    serializer_class = serializers.ItemSerializer

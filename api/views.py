from rest_framework import generics

from api.utils import (
    calculate_trolley_total_price,
    delete_trolley_items,
    process_order,
    remove_item_from_basket_update_or_create_trolley,
)
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
        serializer.validated_data['total_price'] = calculate_trolley_total_price(item_ids)
        serializer.save(user=user, items=item_ids, total_price=serializer.validated_data['total_price'])

        return super(TrolleyAddListView, self).create(serializer)


class TrolleyChangeView(generics.RetrieveUpdateAPIView):
    serializer_class = _serializers.TrolleySerializer
    queryset = models.Trolley.objects.all()

    def perform_update(self, serializer):
        user = self.request.user
        item_ids = serializer.validated_data['items']
        serializer.validated_data['total_price'] = calculate_trolley_total_price(item_ids)
        serializer.save(user=user, items=item_ids, total_price=serializer.validated_data['total_price'])

        return super(TrolleyChangeView, self).perform_update(serializer)


class OrderAddView(generics.CreateAPIView):
    serializer_class = _serializers.OrderSerializer

    def get_queryset(self):
        queryset = models.Order.objects.filter(user=self.request.user, status='complete')

        return queryset

    def perform_create(self, serializer):
        user = self.request.user
        serializer.validated_data['user'] = user
        vouchers = serializer.validated_data['vouchers']
        payment_method = serializer.validated_data['payment_method']
        order_status, total_to_pay, items = process_order(user, vouchers, payment_method)
        serializer.validated_data['items'] = items
        serializer.validated_data['total_paid'] = total_to_pay
        serializer.validated_data['status'] = order_status
        delete_trolley_items(user, order_status, total_to_pay)
        serializer.save(
            user=user,
            items=serializer.validated_data['items'],
            vouchers=vouchers,
            total_paid=total_to_pay,
            payment_method=payment_method,
            status=order_status,
        )

        return super(OrderAddView, self).create(serializer)

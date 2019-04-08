from decimal import Decimal
from api import models


def trolley_items(user):
    return models.Trolley.objects.filter(user=user).exclude(items=[])


def delete_trolley_items(user, order_status, order_amount):
    if order_status == 'complete' and order_amount > Decimal():
        if trolley_items(user).exists():
            trolley_items().first().items.delete()


def remove_item_from_basket_update_or_create_trolley(user, updated_item_ids):
    previous_items = models.Basket.objects.get(user=user).items
    updated_items = models.Item.objects.filter(id__in=updated_item_ids)
    total_price = Decimal()

    if len(updated_items) < len(previous_items):
        for item in updated_items:
            total_price += item.price
        items_to_add = list(set(previous_items) - set(updated_item_ids))
        if models.Trolley.objects.filter(user=user).exists():
            models.Trolley.objects.filter(user=user).update(
                items=items_to_add,
                total_price=total_price,
            )
        else:
            models.Trolley.objects.create(
                user=user,
                items=items_to_add,
                total_price=total_price,
            )


def calculate_trolley_total_price(item_ids):
    total = Decimal()
    if not item_ids:
        return Decimal()
    items = models.Item.objects.filter(id__in=item_ids)
    for item in items:
        total += item.price

    return total


def calculate_total_to_pay(user, vouchers):
    total_to_pay = Decimal()
    full_price_item_cost = Decimal()
    discounted_item_cost = Decimal()
    if trolley_items(user).exists():
        items = models.Item.objects.filter(id__in=trolley_items(user))
        total_discount_rate = calculate_vouchers_rate(vouchers)
        for item in items:
            if not item.discounted:
                full_price_item_cost += item.price
            else:
                discounted_item_cost += item.price
    total_to_pay = full_price_item_cost + (discounted_item_cost - (discounted_item_cost * total_discount_rate))

    return total_to_pay


def payment_method_is_valid(payment_method):
    if not payment_method:
        status = 'incomplete'
    else:
        if payment_method.lower() not in ['card', 'paypal']:
            status = 'incomplete'
        else:
            status = 'complete'

    return status


def calculate_vouchers_rate(vouchers):
    total_discount_rate = Decimal()
    if models.Voucher.objects.all().exists():
        if not vouchers:
            return Decimal()
        else:
            valid_voucher_codes = models.Voucher.objects.all().values_list('code', flat=True)
            for voucher in vouchers:
                if voucher.code in valid_voucher_codes:
                    total_discount_rate += voucher.discounted_rate
                    voucher.delete()
    return total_discount_rate


def process_order(user, vouchers, payment_method):
    order_status = payment_method_is_valid(payment_method)
    total_to_pay = calculate_total_to_pay(user, vouchers)
    items = []
    if trolley_items(user).exists():
        items = trolley_items(user).first().items

    return order_status, total_to_pay, items



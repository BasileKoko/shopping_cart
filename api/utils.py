from decimal import Decimal

from api import models


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
    items = models.Item.objects.filter(id__in=item_ids)
    for item in items:
        total += item.price

    return total

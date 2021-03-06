# Generated by Django 2.2 on 2019-04-06 08:58

from django.db import migrations
from decimal import Decimal
from django.conf import settings


def preload_data(apps, schema_editor):
    Item = apps.get_model('api', 'Item')

    items = (
        {'price': Decimal('28.57'), 'discounted': False},
        {'price': Decimal('15.36'), 'discounted': False},
        {'price': Decimal('118.53'), 'discounted': True},
        {'price': Decimal('58.75'), 'discounted': False},
        {'price': Decimal('8.20'), 'discounted': False},
        {'price': Decimal('725.00'), 'discounted': True},
    )
    for item in items:
        Item.objects.create(
            price=item.get('price'),
            discounted=item.get('discounted'),
        )


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(preload_data),
    ]

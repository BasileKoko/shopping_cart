# Generated by Django 2.2 on 2019-04-08 08:37

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_auto_20190407_2323'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='total_paid',
            field=models.DecimalField(blank=True, decimal_places=2, default=Decimal('0'), max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='voucher',
            name='discounted_rate',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
    ]
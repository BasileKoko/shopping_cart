from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=250),
    price = models.DecimalField(max_digits=5, decimal_places=2)
    discounted = models.BooleanField(default=False)


class Voucher(models.Model):
    code = models.CharField(max_length=250)
    discounted_rate = models.DecimalField(max_digits=5, decimal_places=2)


class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    items = ArrayField(models.IntegerField(null=True, blank=True), null=True, blank=True)


class Trolley(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    items = ArrayField(models.IntegerField(null=True, blank=True), null=True, blank=True)

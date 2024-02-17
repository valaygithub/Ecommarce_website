from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Products(models.Model):
    CAT = (
        (1, "birthday"),
        (2, "anniversary"),
        (3, "Rakhi"),
        (4, "unique"),
        (5, "firhim"),
        (6, "forher"),
    )
    name = models.CharField(max_length=50)
    price = models.FloatField()
    pdetail = models.CharField(max_length=100, verbose_name="Product name")
    category = models.IntegerField(choices=CAT)
    is_active = models.BooleanField(default=True, verbose_name="available")
    pimage = models.ImageField(upload_to="image")

    def __str__(self):
        return self.name


class Cart(models.Model):
    uid = models.ForeignKey(User, on_delete=models.CASCADE, db_column="uid")
    pid = models.ForeignKey(Products, on_delete=models.CASCADE, db_column="pid")
    qty = models.IntegerField(default=1)


class Order(models.Model):
    order_id = models.CharField(max_length=50)
    uid = models.ForeignKey(User, on_delete=models.CASCADE, db_column="uid")
    pid = models.ForeignKey(Products, on_delete=models.CASCADE, db_column="pid")
    qty = models.IntegerField(default=1)

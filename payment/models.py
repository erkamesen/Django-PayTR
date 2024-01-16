from django.db import models
from food.models import Cart
from django.contrib.auth.models import User
from food.models import Product
import random
from food.models import CartItem
# Create your models here.


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    basket = models.ForeignKey(Cart, on_delete=models.CASCADE)
    order_id = models.IntegerField()
    total = models.DecimalField(max_digits=7, decimal_places=2)
    is_paid = models.BooleanField(default=False)
    products = models.ManyToManyField(Product, through='OrderItem')
    order_state = models.CharField(max_length=20, choices=[
        ("Ödeme Bekliyor", "Ödeme Bekliyor"),
        ("Hazırlanıyor", "Hazırlanıyor"),
        ("Yolda", "Yolda"),
        ("Teslim Edildi", "Teslim Edildi")], default="Ödeme Bekliyor")
    order_date = models.DateTimeField(auto_now_add=True)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.basket.user.username} - {self.product.name}"

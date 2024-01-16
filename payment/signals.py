from .models import Order
from food.models import Cart, CartItem
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver




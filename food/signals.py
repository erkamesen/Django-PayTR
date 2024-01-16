from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from .models import Product, Cart, CartItem
from users.models import User
import os
from django.utils import timezone


@receiver(signal=post_delete, sender=Product)
def remove_product_image(sender, instance, **kwargs):
    os.remove(instance.image.path)


@receiver(signal=post_save, sender=User)
def create_cart(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(user=instance)


@receiver(signal=post_delete, sender=User)
def remove_cart(sender, instance, **kwargs):
    cart = Cart.objects.filter(user=instance).first()
    if cart:
        cart.delete()


@receiver(signal=post_delete, sender=User)
def remove_cart_items(sender, instance, **kwargs):
    cart = Cart.objects.filter(user=instance).first()
    items = CartItem.objects.filter(basket=cart).prefetch_related("product")
    for item in items:
        try:
            item.delete()
        except:
            with open("logs/deleted_cart_items.log", "a", encoding="utf-8") as f:
                f.write(
                    f"---\n{instance.username} deleted on {timezone.now()}. but there is something problem with {item}.\n---\n")

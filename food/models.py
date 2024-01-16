from django.db import models
from PIL import Image
from django.contrib.auth.models import User
from users.models import Profile
from django.urls import reverse
# Create your models here.


class Product(models.Model):
    owner = models.ForeignKey(
        User, on_delete=models.SET_DEFAULT, default=1, related_name="owner")
    name = models.CharField(max_length=250)
    description = models.CharField(max_length=250)
    price = models.CharField(max_length=1000)
    image = models.ImageField(
        default="default.png", blank=True, null=True, upload_to="food/%Y/%m/%d/")

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def save(self, *args, **kwargs) -> None:
        super().save(*args, **kwargs)
        imag = Image.open(self.image.path)
        output_size = (300, 300)
        imag.thumbnail(output_size)
        imag.save(self.image.path)

    def get_absolute_url(self):
        return reverse("food:product", kwargs={"pk": self.pk})

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='CartItem')

    def __str__(self) -> str:
        return f"Cart - {self.user.username}"

    def get_total(self):
        items = CartItem.objects.filter(
            basket=self).prefetch_related("product")
        return sum(list(map(lambda x: int(x.product.price), items)))


class CartItem(models.Model):
    basket = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.basket.user.username} - {self.product.name}"

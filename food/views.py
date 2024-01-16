from typing import Any
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from .models import Product, CartItem, Cart
from .forms import ProductForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import list, detail, edit
from django.utils.decorators import method_decorator
# Create your views here.


class IndexListView(list.ListView):
    model = Product
    template_name = "index.html"
    context_object_name = "products"


class ProductDetailView(detail.DetailView):
    model = Product
    template_name = "product/product.html"
    context_object_name = "product"


@method_decorator(login_required, name='dispatch')
class ProductCreateView(edit.CreateView):
    model = Product
    fields = ["name", "description", "price", "image"]
    template_name = "product/product-form.html"

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


@login_required
def create_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('food:main')  #  view name
    else:
        form = ProductForm()
        context = {
            "form": form,
        }
    return render(request, "product/product-form.html", context)


@login_required
def update_product(request, id):
    product = Product.objects.get(id=id)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('food:main')  #  view name
    else:
        form = ProductForm(instance=product)
    context = {
        "form": form,
    }
    return render(request, "product/product-form.html", context)


@login_required
def delete_product(request, id):
    product = Product.objects.get(id=id)
    if request.method == "POST":
        product.delete()
        return redirect('food:main')
    context = {
        "product": product
    }
    return render(request, "product/product-delete.html", context)


@login_required
def cart(request):

    user = request.user
    user_cart = Cart.objects.filter(user=user).first()
    items = CartItem.objects.filter(basket=user_cart).all()
    total_price = user_cart.get_total()
    context = {
        "items": items,
        "total_price": total_price,
    }
    return render(request, "product/cart.html", context)


@login_required
def add_to_cart(request, id):
    product = Product.objects.get(id=id)
    user = request.user
    user_cart = Cart.objects.filter(user=user).first()
    CartItem.objects.create(basket=user_cart, product=product)
    return redirect('food:cart')

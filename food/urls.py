from django.urls import path
from . import views

app_name = "food"
urlpatterns = [
    path('', views.IndexListView.as_view(), name="main"),
    path("<int:pk>/", views.ProductDetailView.as_view(), name="product"),
    path("add/", views.ProductCreateView.as_view(), name="create-product"),
    path("update/<int:id>/", views.update_product, name="update-product"),
    path("delete/<int:id>/", views.delete_product, name="delete-product"),
    path("cart/", views.cart, name="cart"),
    path("add-to-cart/<int:id>/", views.add_to_cart, name="add-to-cart"),
]

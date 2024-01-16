from django.urls import path
from . import views

app_name = "payment"
urlpatterns = [
    path('', views.create_payment, name="create-payment"),
    path('success/', views.success, name="success"),
    path('fail/', views.fail, name="fail"),
]

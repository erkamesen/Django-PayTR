from django.shortcuts import render
from dotenv import load_dotenv
from django.contrib.auth.decorators import login_required
from users.models import Profile
from food.models import Product, CartItem, Cart
from .utils import complete_only
from .models import Order
from django.contrib.auth.models import User
import os
import base64
import hmac
import hashlib
import requests
import json
import random
# Create your views here.

load_dotenv()

merchant_id = str(os.getenv("merchant_id"))
merchant_key = os.getenv("merchant_key").encode()
merchant_salt = os.getenv("merchant_salt").encode()


@complete_only
@login_required
def create_payment(request):
    user = request.user
    user_cart = Cart.objects.filter(user=user).first()
    items = CartItem.objects.filter(
        basket=user_cart).prefetch_related("product")
    if not user_cart:
        context = {
            "reason": "Sepet Bulunamadı."
        }
        print("kart yok")
        return render(request, "payment/payment-fail.html", context=context)
    if not items:
        context = {
            "reason": "Sepet Boş."
        }
        print("itemler yok")
        return render(request, "payment/payment-fail.html", context=context)

    # Adres ve kullanıcı bilgileri burdan alınır.
    profile = Profile.objects.filter(user=user).first()

    email = "erkamesen789@gmail.com"  # profile.email & user.email

    payment_amount = user_cart.get_total()*100
    merchant_oid = str(random.randint(1, 9999999999))
    user_name = user.username
    user_address = profile.address
    user_phone = profile.phone
    merchant_ok_url = 'http://127.0.0.1:8000/payment/success'
    merchant_fail_url = 'http://127.0.0.1:8000/payment/fail'
    item_response = [[item.product.name, item.product.price, 1]
                     for item in items]
    user_basket = base64.b64encode(json.dumps(item_response).encode())
    user_ip = "149.86.143.220"

    timeout_limit = 30
    debug_on = 1
    test_mode = 1

    no_installment = 0
    max_installment = 0

    currency = 'TL'

    hash_str = (
        merchant_id
        + user_ip
        + merchant_oid
        + email
        + str(payment_amount)
        + user_basket.decode()
        + str(no_installment)
        + str(max_installment)
        + currency
        + str(test_mode)
    )
    paytr_token = base64.b64encode(hmac.new(
        merchant_key, hash_str.encode() + merchant_salt, hashlib.sha256).digest())

    params = {
        'merchant_id': merchant_id,
        'user_ip': user_ip,
        'merchant_oid': merchant_oid,
        'email': email,
        'payment_amount': payment_amount,
        'paytr_token': paytr_token,
        'user_basket': user_basket,
        'debug_on': debug_on,
        'no_installment': no_installment,
        'max_installment': max_installment,
        'user_name': user_name,
        'user_address': user_address,
        'user_phone': user_phone,
        'merchant_ok_url': merchant_ok_url,
        'merchant_fail_url': merchant_fail_url,
        'timeout_limit': timeout_limit,
        'currency': currency,
        'test_mode': test_mode
    }

    result = requests.post('https://www.paytr.com/odeme/api/get-token', params)
    res = json.loads(result.text)

    if res['status'] == 'success':
        print(res['token'])
        new_order = Order(user=user, basket=user_cart, total=payment_amount, is_paid=True,
                          order_id=merchant_oid,  order_state="Hazırlanıyor")

        new_order.save()
        context = {
            'token': res['token']
        }
        return render(request, "payment/payment-form.html", context=context)

    else:
        print(result.text)
        return render(request, "payment/payment-fail.html")


def success(request):
    return render(request, "payment/success.html")


def fail(request):
    return render(request, "payment/fail.html")

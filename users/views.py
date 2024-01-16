from django.shortcuts import render, redirect
from .forms import RegisterForm, ProfileForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile
# Create your views here.


def register(request):

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(
                request, f"Welcome {username}, account is created!!")
            return redirect("login")
    form = RegisterForm()
    context = {
        "form": form
    }
    return render(request, "user/register.html", context)


@login_required
def profile(request):
    return render(request, "user/profile.html")


@login_required
def complete_profile(request):
    form = ProfileForm()
    user = request.user
    if request.method == "POST":
        form = ProfileForm(request.POST)
        profile = Profile.objects.filter(user=user).first()
        phone = form.data.get("phone")
        address = form.data.get("address")
        if phone and address:
            profile.phone = phone
            profile.address = address
            profile.is_complete = True
            profile.save()
            return redirect("food:main")
        else:
            messages.warning("Please enter valid datas.")
    context = {
        "form": form,
    }
    return render(request, "user/complete.html", context=context)

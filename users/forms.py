from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from django import forms
from django.http import request


class RegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=200)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["phone", "address"]

    def save(self, commit=True, *args, **kwargs):
        instance = super(ProfileForm, self).save(commit=False, *args, **kwargs)
        instance.is_complete = True
        if commit:
            instance.save()
        return instance

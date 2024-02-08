from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms

#
# class UserRegisterForm(UserCreationForm):
#     email = forms.EmailField()
#
#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password1', 'password2']
#



# forms.py
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Biens

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class BiensCreationForm(forms.ModelForm):
    class Meta:
        model = Biens
        fields = '__all__'

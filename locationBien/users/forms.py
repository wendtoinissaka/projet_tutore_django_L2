from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Biens
from .models import CustomUser

#
# class UserRegisterForm(UserCreationForm):
#     email = forms.EmailField()
#
#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password1', 'password2']



class UserRegisterForm(UserCreationForm):
    nom = forms.CharField(max_length=100)
    numero_tel = forms.CharField(max_length=15)
    email = forms.EmailField()

    class Meta:
        model = CustomUser
        fields = ['username', 'nom', 'numero_tel', 'email', 'password1', 'password2', 'type']


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'nom', 'numero_tel', 'email']  # Champs que l'utilisateur peut mettre à jour








class BiensCreationForm(forms.ModelForm):
    class Meta:
        model = Biens
        fields = '__all__'

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Biens, Avis
from .models import CustomUser
from django.contrib.auth.forms import AuthenticationForm

#
# class UserRegisterForm(UserCreationForm):
#     email = forms.EmailField()
#
#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(label="Password", max_length=30, widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))


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
        exclude = ('proprietaire',)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.request and self.request.user.is_authenticated:
            instance.proprietaire = self.request.user
        if commit:
            instance.save()
        return instance
# class BiensCreationForm(forms.ModelForm):
#     class Meta:
#         model = Biens
#         exclude = ['proprietaire']
#
#



class AvisForm(forms.ModelForm):
    class Meta:
        model = Avis
        exclude = ('created_at', 'bien', 'locataire')
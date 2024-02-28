from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Biens, Avis
from .models import CustomUser
from django.contrib.auth.forms import AuthenticationForm
from .models import Reservation
#
# class UserRegisterForm(UserCreationForm):
#     emails = forms.EmailField()
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
        fields = ['username', 'nom', 'numero_tel', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'nom', 'numero_tel', 'email']  # Champs que l'utilisateur peut mettre à jour


class BiensCreationForm(forms.ModelForm):
    class Meta:
        model = Biens
        exclude = ('proprietaire','date_disponibilite_debut', 'date_disponibilite_fin', 'etat')

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



class ReservationForm(forms.ModelForm):
    # class Meta:
    #     model = Reservation
    #     fields = ['debut_reservation', 'date_fin']  # Ajoutez les champs de date de début et de fin
    class Meta:
        model = Reservation
        fields = ['debut_reservation', 'fin_reservation']
        widgets = {
            'debut_reservation': forms.DateInput(attrs={'type': 'date'}),
            'fin_reservation': forms.DateInput(attrs={'type': 'date'}),
        }




class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['nom', 'numero_tel', 'email', 'password']  # Ajoutez d'autres champs au besoin




class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    # subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)


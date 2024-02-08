from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegisterForm, BiensCreationForm
from .models import Biens
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.http import Http404
from django.contrib.auth import logout
from django.shortcuts import redirect

def create_product(request):
    if request.method == 'POST':
        form = BiensCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home_without_filter')  # Rediriger vers la liste des produits après création
    else:
        form = BiensCreationForm()

    return render(request, 'users/create_product.html', {'form': form})



def home_without_filter(request):
    # biens = Biens.objects.all().order_by('-date_created')
    produits = Biens.objects.all().order_by('-date_created')
    return render(request, 'users/home.html', {'biens': produits})


def home_with_filter(request):
    category = request.GET.get('category', 'all')  # Récupérer la valeur de la catégorie depuis l'URL
    if category == 'all':
        biens = Biens.objects.all().order_by('-date_created')  # Ordre décroissant par date de création
    else:
        biens = Biens.objects.filter(categories=category).order_by('-date_created')
    return render(request, 'users/filter_page.html', {'biens_a_filtrer': biens, 'category': category})

def detail_bien(request, bien_id):
    bien = Biens.objects.get(pk=bien_id)
    return render(request, 'users/detail_bien.html', {'bien': bien})


def do_reservation(request, bien_id):
    reservation = Biens.objects.get(pk=bien_id)
    return render(request, 'users/do_reservation.html', {'reservation': reservation})





def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Hi {username}, your account was created successfully')
            return redirect('home_without_filter')
    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form})


# def custom_logout(request):
#     logout(request)
#     # Ajoutez ici le code pour personnaliser la redirection après la déconnexion
#     return redirect('logout')

@login_required()
def profile(request):
    return render(request, 'users/profile.html')



def erreur(request):
    return render(request, 'users/404.html')


def chackout(request):
    return render(request, 'users/chackout.html')



def error_404_view(request, exeception):
    """
    Vue pour afficher une page d'erreur 404 personnalisée.
    """
    context = {
        # Ajoutez des variables de contexte pour personnaliser la page d'erreur
    }
    return render(request, '404.html', context, status=404)


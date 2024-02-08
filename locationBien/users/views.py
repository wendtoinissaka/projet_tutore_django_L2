from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegisterForm
from .models import Biens
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.http import Http404

def home_without_filter(request):
    biens = Biens.objects.all()
    return render(request, 'users/home.html', {'biens' : biens})


# class BienListView(ListView):
#     model = Biens
#     template_name = 'bien_list.html'
#     context_object_name = 'biens'
#
#     def get_queryset(self):
#         queryset = super().get_queryset()
#         # Filtrer les biens en fonction du paramètre de recherche dans l'URL
#         category = self.request.GET.get('category')
#         if category:
#             queryset = queryset.filter(categories=category)
#         return queryset
#

# def home(request):
#     category = request.GET.get('category')
#     if category:
#         biens = Biens.objects.filter(categories=category)
#     else:
#         biens = Biens.objects.all()
#
#     context = {'biens': biens}
#     return render(request, 'users/home.html', context)
#


# views.py

def home_with_filter(request):
    category = request.GET.get('category', 'all')  # Récupérer la valeur de la catégorie depuis l'URL
    if category == 'all':
        biens = Biens.objects.all()
    else:
        biens = Biens.objects.filter(categories=category)
    return render(request, 'users/home.html', {'biens': biens, 'category': category})

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
            return redirect('home')
    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form})


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


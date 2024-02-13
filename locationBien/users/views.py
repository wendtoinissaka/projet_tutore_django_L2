from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegisterForm, BiensCreationForm, UserUpdateForm, AvisForm
from .models import Biens
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.http import Http404, HttpResponseRedirect
from django.contrib.auth import logout
from django.shortcuts import redirect

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import LoginForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from .models import Biens
from django.utils.translation import gettext as _



from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import DeleteView
from django.views.generic.edit import UpdateView



def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('profile')  # Rediriger vers la page de profil ou toute autre page après la connexion réussie
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})

# def user_login(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#             user = authenticate(request, username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 return redirect('profile')  # Rediriger vers la page de profil ou toute autre page après la connexion réussie
#     else:
#         form = LoginForm()
#     return render(request, 'users/login.html', {'form': form})
#



@login_required()
def create_product(request):
    if request.method == 'POST':
        form = BiensCreationForm(request.POST, request.FILES, request=request)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    else:
        form = BiensCreationForm(request=request)

    return render(request, 'users/create_product.html', {'form': form})
def home_without_filter(request):
#     # biens = Biens.objects.all().order_by('-date_created')
#     produits = Biens.objects.all().order_by('-date_created')
#     return render(request, 'users/home.html', {'biens': produits})
    # Récupérer tous les biens
    biens = Biens.objects.all().order_by('-date_created')

    # Filtrer les biens en fonction de la catégorie (si spécifiée dans la requête GET)
    category = request.GET.get('category')
    if category and category != 'all':
        biens = biens.filter(categories=category).order_by('-date_created')

    return render(request, 'users/home.html', {'biens': biens, 'category': category})


def home_with_filter(request):
    category = request.GET.get('category', 'all')  # Récupérer la valeur de la catégorie depuis l'URL
    if category == 'all':
        biens = Biens.objects.all().order_by('-date_created')  # Ordre décroissant par date de création
    else:
        biens = Biens.objects.filter(categories=category).order_by('-date_created')
    return render(request, 'users/filter_page.html', {'biens_a_filtrer': biens, 'category': category})

# def detail_bien(request, bien_id):
#     bien = Biens.objects.get(pk=bien_id)
#     return render(request, 'users/detail_bien.html', {'bien': bien})

def detail_bien(request, bien_id):
    bien = Biens.objects.get(pk=bien_id)
    total_images = sum([bool(getattr(bien, attr)) for attr in [
        'image_principale', 'image_facultative_1', 'image_facultative_2']])
    images = []
    for i in range(total_images):
        attr = f"image_principale" if i == 0 else f"image_facultative_{i}"
        if hasattr(bien, attr):
            images.append(getattr(bien, attr))
    return render(request, 'users/detail_bien.html', {'bien': bien, 'images': images})


# def detail_bien(request, bien_id):
#     bien = Biens.objects.get(id=bien_id)
#     images = Images.objects.filter(bien=bien)
#     context = {"bien": bien, "images": images}
#     return render(request, "users/detail_bien.html", context)

# def details(request):
#     return render(request, 'users/detail_bien.html')





def do_reservation(request, bien_id):
    reservation = Biens.objects.get(pk=bien_id)
    return render(request, 'users/do_reservation.html', {'reservation': reservation})


# def custom_logout(request):
#     logout(request)
#     # Ajoutez ici le code pour personnaliser la redirection après la déconnexion
#     return redirect('logout')

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



@login_required()
def profile(request):
    return render(request, 'users/profile.html')









def user_update(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Rediriger vers la page du profil de l'utilisateur après la mise à jour
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, 'users/user_update.html', {'form': form})


def erreur(request):
    return render(request, 'users/404.html')




def error_404_view(request, exeception):
    """
    Vue pour afficher une page d'erreur 404 personnalisée.
    """
    context = {
        # Ajoutez des variables de contexte pour personnaliser la page d'erreur
    }
    return render(request, '404.html', context, status=404)


def header(request):
    return render(request, 'users/header.html')

# @login_required
# def list_user_bien(request):
#     user = request.user
#     biens = Biens.objects.filter(proprietaire=user)
#     context = {'biens': biens}
#     return render(request, 'users/list_user_bien.html', context)


# Dans views.py

@login_required()
def list_user_bien(request):
    # Récupérer les biens de l'utilisateur connecté
    user_biens = Biens.objects.filter(proprietaire=request.user).order_by('-date_created')

    # Filtrer les biens en fonction de la catégorie (si spécifiée dans la requête GET)
    category = request.GET.get('category')
    if category and category != 'all':
        user_biens = user_biens.filter(categories=category).order_by('-date_created')

    return render(request, 'users/list_user_bien.html', {'user_biens': user_biens, 'category': category})


@method_decorator(login_required, name='dispatch')
class ListUserBienView(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        user_biens = Biens.objects.filter(proprietaire=user).order_by('-date_created')
        return render(request, 'users/list_user_bien.html', {'user_biens': user_biens})



def ajouter_avis(request):
    if request.method == 'POST':
        form = AvisForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home_without_filter')
    else:
        form = AvisForm()
    return render(request, 'users/ajouter_avis.html', {'form': form})

class EditBienView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Biens
    fields = ['nom', 'etat', 'categories', 'localisation', 'description', 'prix', 'image_principale', 'image_facultative_1', 'image_facultative_2', 'image_facultative_3' ]  # Liste des champs que vous souhaitez modifier
    template_name = 'users/edit_bien.html'
    success_message = _("Le bien a été modifié avec succès.")

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.proprietaire != request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('detail_bien', args=[self.object.id])



class DeleteBienView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Biens
    template_name = 'users/confirm_delete_bien.html'
    success_message = _("Le bien a été supprimé avec succès.")
    success_url = reverse_lazy('list_user_bien')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.proprietaire != request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
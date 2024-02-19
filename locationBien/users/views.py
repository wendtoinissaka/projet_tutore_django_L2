from datetime import datetime, timedelta
from importlib.resources import _
from io import BytesIO
from celery import shared_task
from bs4.builder import HTML
from bs4.css import CSS
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied
from django.core.files.base import ContentFile
from django.core.mail import EmailMessage, EmailMultiAlternatives, send_mail
from django.db import transaction
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.utils.html import strip_tags
from django.views import View
from django.views.generic import UpdateView, DeleteView, CreateView

from .forms import UserRegisterForm, BiensCreationForm, UserUpdateForm, AvisForm, ReservationForm, LoginForm, \
    CustomUserForm
from .models import Biens, Reservation, Payment, CustomUser
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import io
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

# Add these lines to import necessary components from WeasyPrint
from weasyprint import HTML, CSS

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



# def do_reservation(request, bien_id):
#     reservation = Biens.objects.get(pk=bien_id)
#     return render(request, 'users/do_reservation.html', {'reservation': reservation})


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

@login_required
def updateProfile(request):
    user = request.user
    if request.method == 'POST':
        form = CustomUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('updateProfile')  # Rediriger vers la page de profil après la mise à jour
    else:
        form = CustomUserForm(instance=user)
    return render(request, 'users/updateProfile.html', {'form': form})








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


@login_required
def reservation_detail(request, reservation_id):
    reservation = get_object_or_404(Reservation, pk=reservation_id)
    payment_expired = reservation.is_payment_expired()
    return render(request, 'users/reservation_detail.html', {'reservation': reservation, 'payment_expired': payment_expired})

@login_required
def reservation_page(request):
    # Récupérer les réservations de l'utilisateur connecté
    reservations = Reservation.objects.filter(locataire=request.user, status='en_attente')
    return render(request, 'users/reservation_page.html', {'reservations': reservations})
# @login_required
# def do_reservation(request, bien_id):
#     bien = get_object_or_404(Biens, pk=bien_id)
#     if bien.etat != 'disponible':
#         messages.error(request, "Le bien n'est pas disponible pour le moment.")
#         return redirect('detail_bien', bien_id=bien.id)
#
#     if request.method == 'POST':
#         form = ReservationForm(request.POST)
#         if form.is_valid():
#             reservation = form.save(commit=False)
#             reservation.bienloue = bien
#             reservation.locataire = request.user
#             reservation.proprietaire = bien.proprietaire
#             reservation.prix_total = bien.prix * reservation.nombre_jours
#             reservation.save()
#
#             # Mettre à jour l'état du bien en réservation_en_cours et la date d'expiration du paiement
#             bien.etat = 'en_cours'
#             bien.date_disponibilite_debut = None
#             bien.date_disponibilite_fin = None
#             bien.save()
#
#             # Définir la date d'expiration du paiement à 30 minutes à partir de maintenant
#             reservation.date_expiration_paiement = timezone.now() + timezone.timedelta(minutes=30)
#             reservation.save()
#
#             # Envoyer l'email de confirmation
#             now = datetime.now()
#             tomorrow = now + timedelta(days=1)
#             subject = "Confirmation de réservation"
#             message = ("Bonjour {}, \n\nVotre réservation pour le bien \"{}\" a été acceptée. \n\nLes détails de votre réservation sont:\n\nNuméro de réservation: {}\nLocataire: {}\nPropriétaire: {}\nBien: {}\nDates de location: {}\nNombres de nuits: {}\nMontant total: {}\nDate d'expiration du paiement: {}\n\nCordialement,\nL'équipe CAPADATA".format(request.user.username, bien.nom, reservation.id, request.user.username, bien.proprietaire, bien.nom, form.cleaned_data['datedebut'], form.cleaned_data['nombre_jours'], reservation.prix_total, reservation.date_expiration_paiement))
#
#             email = EmailMessage(subject, message, settings.EMAIL_HOST_USER, [request.user.email])
#             email.send()
#
#             return redirect('reservation_detail', reservation_id=reservation.id)
#     else:
#         form = ReservationForm()
#
#     return render(request, 'users/create_reservation.html', {'form': form, 'bien': bien})



# Add this utility function above the views definitions
# def generate_pdf(html_string):
#     """Use WeasyPrint library to convert HTML to PDF."""
#     weasyprint_cfg = {
#         "enable-local-file-access": None,
#         "default-encoding": "utf-8",
#         "hide-link-targets": None,
#         "javascript-delay": 2000,
#         "image-quality": 90,
#         "media-query-mode": "strict",
#         "outline-depth": 7,
#         "footer-rules": "-s footer-right:'Page [[page]] of [[topage]]';",
#     }
#     pdf_bytes = HTML(string=html_string).write_pdf(stylesheets=[CSS(string='body {font-size: 12pt;}')], presentational_hints=True, **weasyprint_cfg)
#     return BytesIO(pdf_bytes)

# def generate_pdf(html_string):
#     """Generate a PDF file from the given HTML string."""
#     css = CSS(string='body {font-size: 12pt;}')
#     html = HTML(string=html_string, base_url='none')
#     weasyprint_cfg = {
#         "enable-local-file-access": None,
#         "default-encoding": "utf-8",
#         "hide-link-targets": None,
#         "javascript-delay": 2000,
#         "image-quality": 90,
#         "media-query-mode": "strict",
#         "outline-depth": 7,
#         "footer-rules": "-s footer-right:'Page [[page]] of [[topage]]';",
#     }
#     pdf_bytes = html.write_pdf(stylesheets=[css], presentational_hints=True, **weasyprint_cfg)
#
#     return io.BytesIO(pdf_bytes)


@login_required
def do_reservation(request, bien_id):
    bien = get_object_or_404(Biens, pk=bien_id)
    if bien.etat != 'disponible':
        messages.error(request, "Le bien n'est pas disponible pour le moment.")
        return redirect('detail_bien', bien_id=bien.id)

    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.bienloue = bien
            reservation.locataire = request.user
            reservation.proprietaire = bien.proprietaire
            reservation.prix_total = bien.prix * reservation.nombre_jours
            reservation.save()

            # Mettre à jour l'état du bien en réservation_en_cours et la date d'expiration du paiement
            bien.etat = 'en_cours'
            bien.date_disponibilite_debut = None
            bien.date_disponibilite_fin = None
            bien.save()

            # Définir la date d'expiration du paiement à 24 heures à partir de maintenant
            reservation.date_expiration_paiement = timezone.now() + timezone.timedelta(hours=24)
            reservation.save()

            # Envoyer l'e-mail personnalisé
            subject = "Confirmation de réservation chez Capadata"
            message = render_to_string('users/emails/facture_email.txt', {'bien': bien, 'reservation': reservation, 'total_price': reservation.prix_total})
            html_message = render_to_string('users/emails/email_template.html', {'bien': bien, 'reservation': reservation,  'total_price': reservation.prix_total})
            plain_message = strip_tags(html_message)  # Version texte brut du HTML

            send_mail(subject, plain_message, settings.EMAIL_HOST_USER, [request.user.email], html_message=html_message)

            return redirect('reservation_detail', reservation_id=reservation.id)
    else:
        form = ReservationForm()

    return render(request, 'users/create_reservation.html', {'form': form, 'bien': bien})



# @login_required
# def do_reservation(request, bien_id):
#     bien = get_object_or_404(Biens, pk=bien_id)
#     if bien.etat != 'disponible':
#         messages.error(request, "Le bien n'est pas disponible pour le moment.")
#         return redirect('detail_bien', bien_id=bien.id)
#
#     if request.method == 'POST':
#         form = ReservationForm(request.POST)
#         if form.is_valid():
#             reservation = form.save(commit=False)
#             reservation.bienloue = bien
#             reservation.locataire = request.user
#             reservation.proprietaire = bien.proprietaire
#             reservation.prix_total = bien.prix * reservation.nombre_jours
#             reservation.save()
#
#             # Mettre à jour l'état du bien en réservation_en_cours et la date d'expiration du paiement
#             bien.etat = 'en_cours'
#             bien.date_disponibilite_debut = None
#             bien.date_disponibilite_fin = None
#             bien.save()
#
#             # Définir la date d'expiration du paiement à 30 minutes à partir de maintenant
#             reservation.date_expiration_paiement = timezone.now() + timezone.timedelta(minutes=30)
#             reservation.save()
#
#             # Generate invoice HTML
#             invoice_html = render_to_string('users/invoice_template.html', {'reservation': reservation})
#
#             # Send email with invoice attachment
#             subject = "Invoice for Your Reservation at Capadata"
#             from_email = settings.EMAIL_HOST_USER
#             to_email = [request.user.email]
#             text_content = strip_tags(invoice_html)  # Strip HTML tags for plain text email
#             html_content = invoice_html
#
#             # Create email message with invoice HTML as attachment
#             email_message = EmailMultiAlternatives(subject, text_content, from_email, to_email)
#             email_message.attach_alternative(html_content, "text/html")
#             email_message.send()
#
#             return redirect('reservation_detail', reservation_id=reservation.id)
#     else:
#         form = ReservationForm()
#
#     return render(request, 'users/create_reservation.html', {'form': form, 'bien': bien})



@login_required
def validate_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, pk=reservation_id)

    # Vérifier si la date d'expiration du paiement est passée
    if reservation.date_expiration_paiement < timezone.now():
        # Si la date d'expiration est passée, annuler la réservation et remettre le bien à "disponible"
        reservation.bienloue.etat = 'disponible'
        reservation.bienloue.save()
        reservation.delete()
        return render(request, 'users/reservation_expired.html')

    # Si la date d'expiration n'est pas passée, marquer la réservation comme validée
    reservation.status = 'validee'
    reservation.save()

    # Mettre à jour l'état du bien en "en_cours"
    reservation.bienloue.etat = 'en_cours'
    reservation.bienloue.save()

    return redirect('reservation_detail', reservation_id=reservation.id)


@login_required
@transaction.atomic
def cancel_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)

    if request.method == 'POST':
        if reservation.locataire == request.user and reservation.status != 'annulee':
            reservation.status = 'annulee'
            reservation.save()

            # Restaurer l'état du bien
            bien = reservation.bienloue
            bien.etat = 'disponible'
            bien.date_disponibilite_debut = timezone.now()
            bien.save()

            messages.success(request, "La réservation a été annulée avec succès.")
        else:
            messages.error(request, "Seul le locataire peut annuler cette réservation.")

    return redirect('reservation_page')


@login_required
def confirm_cancel_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, locataire=request.user)
    return render(request, 'users/confirm_cancel_reservation.html', {'reservation': reservation})


class PaymentCreateView(CreateView):
    model = Payment
    fields = ['amount', 'reference']
    success_url = reverse_lazy('reservation_page')

    def form_valid(self, form):
        form.instance.reservation_id = self.kwargs['reservation_id']
        form.instance.paid_by = self.request.user
        return super().form_valid(form)
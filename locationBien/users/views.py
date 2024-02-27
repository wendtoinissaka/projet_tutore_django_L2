from datetime import datetime, timedelta
from decimal import Decimal
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
from django.db.models import Avg
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.utils.html import strip_tags
from django.views import View
from django.views.generic import UpdateView, DeleteView, CreateView
from pip._internal.configuration import Configuration

from .forms import UserRegisterForm, BiensCreationForm, UserUpdateForm, AvisForm, ReservationForm, LoginForm, \
    CustomUserForm, ContactForm
from .models import Biens, Reservation, Payment, CustomUser, Avis
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import io
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

# Add these lines to import necessary components from WeasyPrint
from weasyprint import HTML, CSS
from django.shortcuts import render, redirect
from paypalrestsdk import Payment, configure
from django.urls import reverse
from django.http import HttpResponse

from .tasks import update_bien_state

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
    biens = Biens.objects.all().order_by('-date_created')

    # Filtrer les biens en fonction de la catégorie (si spécifiée dans la requête GET)
    category = request.GET.get('category')
    if category and category != 'all':
        biens = biens.filter(categories=category)# def home_without_filter(request):
#     # Récupérer tous les biens
    # Filtrer les biens en fonction de la recherche (si spécifiée dans la requête GET)#     biens = Biens.objects.all().order_by('-date_created')# def home_without_filter(request):
    search_query = request.GET.get('q')# # #     # biens = Biens.objects.all().order_by('-date_created')
    if search_query:#     # Calculer la moyenne des avis pour chaque bien# #     produits = Biens.objects.all().order_by('-date_created')
        biens = biens.filter(nom__icontains=search_query)#     for bien in biens:# #     return render(request, 'users/home.html', {'biens': produits})
#         bien.moyenne_avis = Avis.objects.filter(bien=bien).aggregate(Avg('note'))['note__avg']#     # Récupérer tous les biens
    return render(request, 'users/home.html', {'biens': biens, 'category': category})# #     biens = Biens.objects.all().order_by('-date_created')





def home_with_filter(request):
    category = request.GET.get('category', 'all')  # Récupérer la valeur de la catégorie depuis l'URL
    if category == 'all':
        biens = Biens.objects.all().order_by('-date_created')  # Ordre décroissant par date de création
    else:
        biens = Biens.objects.filter(categories=category).order_by('-date_created')
    return render(request, 'users/filter_page.html', {'biens_a_filtrer': biens, 'category': category})



from django.db.models import Avg

def detail_bien(request, bien_id):
    bien = Biens.objects.get(pk=bien_id)# def detail_bien(request, bien_id):
    total_images = sum([bool(getattr(bien, attr)) for attr in [#     bien = Biens.objects.get(id=bien_id)
        'image_principale', 'image_facultative_1', 'image_facultative_2']])#     images = Images.objects.filter(bien=bien)
    images = []#     context = {"bien": bien, "images": images}
    for i in range(total_images):#     return render(request, "users/detail_bien.html", context)
        attr = f"image_principale" if i == 0 else f"image_facultative_{i}"
        if hasattr(bien, attr):# def details(request):
            images.append(getattr(bien, attr))#     return render(request, 'users/detail_bien.html')

    # Calculer la moyenne des avis pour le bien spécifique
    moyenne_avis = Avis.objects.filter(bien=bien).aggregate(Avg('note'))['note__avg']
    related_biens = bien.get_related_biens()
# def do_reservation(request, bien_id):
    return render(request, 'users/detail_bien.html', {'bien': bien, 'images': images, 'moyenne_avis': moyenne_avis, 'related_biens': related_biens})#     reservation = Biens.objects.get(pk=bien_id)

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
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Rediriger vers la page de profil après la mise à jour
    else:
        form = UserUpdateForm(instance=user)
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



@login_required
def list_user_bien(request):
    # Récupérer les biens de l'utilisateur connecté
    user_biens = Biens.objects.filter(proprietaire=request.user).order_by('-date_created')

    # Filtrer les biens en fonction de la recherche (si spécifiée dans la requête GET)
    search_query = request.GET.get('q')
    if search_query:
        user_biens = user_biens.filter(nom__icontains=search_query)

    # Filtrer les biens en fonction de la catégorie (si spécifiée dans la requête GET)
    category = request.GET.get('category')
    if category and category != 'all':
        user_biens = user_biens.filter(categories=category).order_by('-date_created')# Dans views.py

    return render(request, 'users/list_user_bien.html', {'user_biens': user_biens, 'category': category})# @login_required()


@method_decorator(login_required, name='dispatch')
class ListUserBienView(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        user_biens = Biens.objects.filter(proprietaire=user).order_by('-date_created')
        return render(request, 'users/list_user_bien.html', {'user_biens': user_biens})


@login_required
def ajouter_avis(request,bien_id):
    bien = get_object_or_404(Biens, pk=bien_id)
    locataire = request.user
    if request.method == 'POST':
        form = AvisForm(request.POST)
        if form.is_valid():
            avis = form.save(commit=False)
            avis.bien = bien
            avis.locataire = locataire
            avis.save()
            return redirect('detail_bien', bien_id=bien_id)  # Redirection vers detail_bien avec bien_id
    else:
        form = AvisForm()
            
    return render(request, 'users/ajouter_avis.html', {'form': form, 'bien': bien})




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


# reservation et paiement





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
#
#             # Calcul du nombre de jours de réservation
#             debut_reservation = form.cleaned_data['debut_reservation']
#             fin_reservation = form.cleaned_data['fin_reservation']
#             nombre_jours = (fin_reservation - debut_reservation).days + 1
#             reservation.nombre_jours = nombre_jours
#
#             # Calcul du prix total en fonction du nombre de jours de réservation
#             reservation.prix_total = bien.prix * nombre_jours
#             reservation.save()
#
#             # Mettre à jour l'état du bien en "en_cours"
#             bien.etat = 'en_cours'
#             bien.save()
#
#             # Définir la date d'expiration du paiement à 15 minutes à partir de maintenant
#             reservation.date_expiration_paiement = timezone.now() + timezone.timedelta(minutes=15)
#             reservation.save()
#
#             # Envoyer l'e-mail personnalisé
#             subject = "Confirmation de réservation chez Capadata"
#             message = render_to_string('users/emails/facture_email.txt', {'bien': bien, 'reservation': reservation, 'total_price': reservation.prix_total})
#             html_message = render_to_string('users/emails/email_template.html', {'bien': bien, 'reservation': reservation,  'total_price': reservation.prix_total})
#             plain_message = strip_tags(html_message)  # Version texte brut du HTML
#
#             send_mail(subject, plain_message, settings.EMAIL_HOST_USER, [request.user.email], html_message=html_message)
#
#             return redirect('reservation_detail', reservation_id=reservation.id)
#     else:
#         form = ReservationForm()
#
#     return render(request, 'users/create_reservation.html', {'form': form, 'bien': bien})


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

            # Calcul du nombre de jours de réservation
            debut_reservation = form.cleaned_data['debut_reservation']
            fin_reservation = form.cleaned_data['fin_reservation']
            nombre_jours = (fin_reservation - debut_reservation).days + 1
            reservation.nombre_jours = nombre_jours

            # Calcul du prix total en fonction du nombre de jours de réservation
            reservation.prix_total = bien.prix * nombre_jours
            reservation.save()

            # Créer une instance de Reservation avec l'état initial et la date d'expiration du paiement
            reservation.status = 'en_attente'
            reservation.date_expiration_paiement = timezone.now() + timezone.timedelta(minutes=15)
            reservation.save()

            # Planifier la mise à jour de l'état du bien après la durée de la réservation
            update_bien_state.apply_async((bien.id,), countdown=nombre_jours * 24 * 60 * 60)

            # Envoyer l'e-mail personnalisé
            subject = "Confirmation de réservation chez Capadata"
            message = render_to_string('users/emails/facture_email.txt', {'bien': bien, 'reservation': reservation,
                                                                          'total_price': reservation.prix_total})
            html_message = render_to_string('users/emails/email_template.html',
                                            {'bien': bien, 'reservation': reservation,
                                             'total_price': reservation.prix_total})
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
#
#             # Calculer le nombre de jours entre la date de début et la date de fin
#             date_debut = form.cleaned_data['debut_reservation']
#             date_fin = form.cleaned_data['fin_reservation']
#             nombre_jours = (date_fin - date_debut).days + 1  # Ajouter 1 car le jour de début est inclus
#             reservation.nombre_jours = nombre_jours
#
#             reservation.prix_total = bien.prix * nombre_jours
#             reservation.save()
#
#             # Mettre à jour l'état du bien en "en_cours"
#             bien.etat = 'en_cours'
#             bien.save()
#
#             # Définir la date d'expiration du paiement à 15 minutes à partir de maintenant
#             reservation.date_expiration_paiement = timezone.now() + timezone.timedelta(minutes=15)
#             reservation.save()
#
#             # Envoyer l'e-mail personnalisé
#             subject = "Confirmation de réservation chez Capadata"
#             message = render_to_string('users/emails/facture_email.txt', {'bien': bien, 'reservation': reservation, 'total_price': reservation.prix_total})
#             html_message = render_to_string('users/emails/email_template.html', {'bien': bien, 'reservation': reservation,  'total_price': reservation.prix_total})
#             plain_message = strip_tags(html_message)  # Version texte brut du HTML
#
#             send_mail(subject, plain_message, settings.EMAIL_HOST_USER, [request.user.email], html_message=html_message)
#
#             return redirect('reservation_detail', reservation_id=reservation.id)
#     else:
#         form = ReservationForm()
#
#     return render(request, 'users/create_reservation.html', {'form': form, 'bien': bien})
#



# @login_required
# def process_payment(request, reservation_id):
#     reservation = Reservation.objects.get(id=reservation_id)
#     montant_initial = reservation.prix_total
#     montant_augmente = montant_initial * Decimal(1.20)
#     montant_reservation = "{:.2f}".format(montant_augmente)
#
#     configure({
#         "mode": "sandbox",
#         "client_id": settings.PAYPAL_CLIENT_ID,
#         "client_secret": settings.PAYPAL_CLIENT_SECRET
#     })
#
#     payment = Payment({
#         "intent": "sale",
#         "payer": {
#             "payment_method": "paypal"
#         },
#         "redirect_urls": {
#             "return_url": request.build_absolute_uri(reverse('execute_payment') + '?reservation_id=' + str(reservation_id)),
#             "cancel_url": request.build_absolute_uri(reverse('cancel_payment') + '?reservation_id=' + str(reservation_id))
#         },
#         "transactions": [{
#             "amount": {
#                 "total": montant_reservation,
#                 "currency": "USD"
#             },
#             "description": "Paiement de réservation"
#         }]
#     })
#
#     if payment.create():
#         for link in payment.links:
#             if link.rel == "approval_url":
#                 # Mettre à jour l'état du bien en "en_cours" et définir la date d'expiration du paiement à 15 minutes à partir de maintenant
#                 bien = reservation.bienloue
#                 bien.etat = 'en_cours'
#                 bien.date_expiration_paiement = timezone.now() + timezone.timedelta(minutes=15)
#                 bien.save()
#                 return redirect(link.href)
#     else:
#         return render(request, 'users/paiement/payment_cancel.html')

@login_required
def process_payment(request, reservation_id):
    reservation = Reservation.objects.get(id=reservation_id)

    if reservation.is_payment_expired():
        # Paiement expiré, remettre l'état du bien à disponible
        reservation.bienloue.etat = 'disponible'
        reservation.bienloue.save()
        return render(request, 'payment_expired.html')

    montant_initial = reservation.prix_total
    montant_augmente = montant_initial * Decimal(1.20)
    montant_reservation = "{:.2f}".format(montant_augmente)

    configure({
        "mode": "sandbox",
        "client_id": settings.PAYPAL_CLIENT_ID,
        "client_secret": settings.PAYPAL_CLIENT_SECRET
    })

    payment = Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"
        },
        "redirect_urls": {
            "return_url": request.build_absolute_uri(reverse('execute_payment') + '?reservation_id=' + str(reservation_id)),
            "cancel_url": request.build_absolute_uri(reverse('cancel_payment') + '?reservation_id=' + str(reservation_id))
        },
        "transactions": [{
            "amount": {
                "total": montant_reservation,
                "currency": "USD"
            },
            "description": "Paiement de réservation"
        }]
    })

    if payment.create():
        for link in payment.links:
            if link.rel == "approval_url":
                # Mettre à jour l'état du bien en "en_cours" et définir la date d'expiration du paiement à 15 minutes à partir de maintenant
                bien = reservation.bienloue
                bien.etat = 'en_cours'
                bien.date_expiration_paiement = timezone.now() + timezone.timedelta(minutes=15)
                bien.save()
                return redirect(link.href)
    else:
        # Paiement échoué, remettre l'état du bien à disponible
        reservation.bienloue.etat = 'disponible'
        reservation.bienloue.save()
        return render(request, 'users/paiement/payment_cancel.html')


@login_required
def execute_payment(request):
    reservation_id = request.GET.get('reservation_id')

    if not reservation_id:
        return HttpResponseNotFound("ID de réservation manquant dans la requête.")

    try:
        reservation = Reservation.objects.get(id=reservation_id)
    except Reservation.DoesNotExist:
        return HttpResponseNotFound("La réservation avec l'ID spécifié n'existe pas.")

    # Vérifiez ici si le paiement a été effectué avec succès et mettez à jour l'état du bien en conséquence

    return redirect('payment_success')  # Redirection vers une page par défaut


@login_required
def cancel_payment(request):
    reservation_id = request.GET.get('reservation_id')
    try:
        reservation = Reservation.objects.get(id=reservation_id)
    except Reservation.DoesNotExist:
        return HttpResponse("La réservation n'existe pas.", status=404)

    bien = reservation.bienloue
    bien.etat = 'disponible'
    bien.save()

    return render(request, 'users/paiement/payment_cancel.html')

def payment_success(request):
    return render(request, 'users/paiement/payment_success.html')

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

    # Planifier la mise à jour de l'état du bien après la durée de la réservation
    update_bien_state.apply_async((reservation.id,), countdown=reservation.nombre_jours * 24 * 60 * 60)

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


# Dans views.py

# Vue pour le processus de paiement


# @login_required
# def cancel_payment(request):
#     reservation_id = request.GET.get('reservation_id')
#     try:
#         reservation = Reservation.objects.get(id=reservation_id)
#     except Reservation.DoesNotExist:
#         # Gérer le cas où la réservation n'existe pas
#         return HttpResponse("La réservation n'existe pas.", status=404)
#
#     bien = reservation.bienloue
#     bien.etat = 'disponible'
#     bien.save()
#
#     return render(request, 'users/paiement/payment_cancel.html')
#



def contactUs(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            send_mail(
                'CAPAB : Location de bien',
                message,
                email,
                ['lacapacitee@gmail.com',settings.EMAIL_HOST_USER],
                fail_silently=False,
            )
            return render(request, 'users/contact_success.html')
    else:
        form = ContactForm()
    return render(request, 'users/contactUs.html', {'form': form})
import json
from datetime import datetime, timedelta
from decimal import Decimal
from importlib.resources import _
from io import BytesIO

import stripe
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
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest, HttpResponseNotFound, JsonResponse
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

from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import UserRegisterForm
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from .models import CustomUser

from django.shortcuts import render
from .models import Biens


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(
                    'profile')  # Rediriger vers la page de profil ou toute autre page après la connexion réussie
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
        biens = biens.filter(categories=category)

    # Filtrer les biens en fonction de l'état du bien (si spécifié dans la requête GET)
    etat = request.GET.get('etat')
    if etat and etat != 'all':
        biens = biens.filter(etat=etat)

    # Filtrer les biens en fonction de la recherche (si spécifiée dans la requête GET)
    search_query = request.GET.get('q')
    if search_query:
        biens = biens.filter(nom__icontains=search_query)

    return render(request, 'users/home.html', {'biens': biens, 'category': category, 'etat': etat})



def home_with_filter(request):
    category = request.GET.get('category', 'all')  # Récupérer la valeur de la catégorie depuis l'URL
    if category == 'all':
        biens = Biens.objects.all().order_by('-date_created')  # Ordre décroissant par date de création
    else:
        biens = Biens.objects.filter(categories=category).order_by('-date_created')
    return render(request, 'users/filter_page.html', {'biens_a_filtrer': biens, 'category': category})


from django.db.models import Avg


def detail_bien(request, bien_id):
    bien = Biens.objects.get(pk=bien_id)  # def detail_bien(request, bien_id):
    total_images = sum([bool(getattr(bien, attr)) for attr in [  # bien = Biens.objects.get(id=bien_id)
        'image_principale', 'image_facultative_1', 'image_facultative_2']])  # images = Images.objects.filter(bien=bien)
    images = []  # context = {"bien": bien, "images": images}
    for i in range(total_images):  # return render(request, "users/detail_bien.html", context)
        attr = f"image_principale" if i == 0 else f"image_facultative_{i}"
        if hasattr(bien, attr):  # def details(request):
            images.append(getattr(bien, attr))  # return render(request, 'users/detail_bien.html')

    # Calculer la moyenne des avis pour le bien spécifique
    moyenne_avis = Avis.objects.filter(bien=bien).aggregate(Avg('note'))['note__avg']
    related_biens = bien.get_related_biens()
    # def do_reservation(request, bien_id):
    return render(request, 'users/detail_bien.html', {'bien': bien, 'images': images, 'moyenne_avis': moyenne_avis,
                                                      'related_biens': related_biens})  # reservation = Biens.objects.get(pk=bien_id)


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Compte inactif jusqu'à confirmation par e-mail
            user.save()

            # Envoi de l'e-mail de confirmation
            current_site = get_current_site(request)
            subject = 'Activation de compte chez CAPADATA'
            message = render_to_string('users/activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])

            messages.success(request, f'Bienvenue! {user.username}, Verifiez votre email pour valider votre compte svp!')
            return redirect('registration_confirmation')
            # return redirect(reverse('registration_confirmation'))
    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form})




def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'users/emails/activation_done.html')
    else:
        return render(request, 'users/emails/activation_invalid.html')

def registration_confirmation(request):
    return render(request, 'users/emails/registration_confirmation.html')


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
    user_biens = Biens.objects.filter(proprietaire=request.user)

    # Filtrer les biens en fonction de la recherche (si spécifiée dans la requête GET)
    search_query = request.GET.get('q')
    if search_query:
        user_biens = user_biens.filter(nom__icontains=search_query)


    # Filtrer les biens en fonction de la catégorie (si spécifiée dans la requête GET)
    category = request.GET.get('category')
    if category and category != 'all':
        user_biens = user_biens.filter(categories=category).order_by('-date_created')  # Dans views.py

    # Filtrer les biens en fonction de l'état (si spécifié dans la requête GET)
    etat = request.GET.get('etat')
    if etat and etat != 'all':
        user_biens = user_biens.filter(etat=etat)

    return render(request, 'users/list_user_bien.html', {'user_biens': user_biens, 'category': category})


@method_decorator(login_required, name='dispatch')
class ListUserBienView(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        user_biens = Biens.objects.filter(proprietaire=user).order_by('-date_created')
        return render(request, 'users/list_user_bien.html', {'user_biens': user_biens})


@login_required
def ajouter_avis(request, bien_id):
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
    fields = ['nom', 'etat', 'categories', 'localisation', 'description', 'prix', 'image_principale',
              'image_facultative_1', 'image_facultative_2',
              'image_facultative_3']  # Liste des champs que vous souhaitez modifier
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
    # reservation.status = 'annulee'
    # reservation.save()
    return render(request, 'users/reservation_detail.html',
                  {'reservation': reservation, 'payment_expired': payment_expired})


# @login_required
# def reservation_page(request):
#     # Récupérer les réservations de l'utilisateur connecté
#     reservations = Reservation.objects.filter(locataire=request.user, status='en_attente')
#     return render(request, 'users/reservation_page.html', {'reservations': reservations})
# @login_required
# def reservation_page(request):
#     # Récupérer le paramètre d'état de la requête GET
#     etat = request.GET.get('etat')
#
#     # Par défaut, filtrer les réservations en attente
#     reservations = Reservation.objects.filter(locataire=request.user)
#
#     # Si un état est spécifié dans la requête, filtrer en conséquence
#     if etat and etat != 'all':
#         reservations = reservations.filter(status=etat)
#
#     return render(request, 'users/reservation_page.html', {'reservations': reservations, 'etat': etat})

@login_required
def reservation_page(request):
    # Récupérer le paramètre d'état de la requête GET
    etat = request.GET.get('etat')

    # Filtrer les réservations en attente
    reservations_en_attente = Reservation.objects.filter(locataire=request.user, status='en_attente')

    # Filtrer les autres réservations selon l'état spécifié dans la requête GET
    reservations_triees = Reservation.objects.filter(locataire=request.user)
    if etat and etat != 'all':
        reservations_triees = reservations_triees.filter(status=etat)

    return render(request, 'users/reservation_page.html', {
        'reservations_en_attente': reservations_en_attente,
        'reservations_triees': reservations_triees,
        'etat': etat
    })


@login_required
def validate_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, pk=reservation_id)

    # Vérifier si la date d'expiration du paiement est passée
    if reservation.date_expiration_paiement < timezone.now():
        # Si la date d'expiration est passée, annuler la réservation et remettre le bien à "disponible"
        reservation.bienloue.etat = 'disponible'
        reservation.bienloue.save()
        reservation.delete()
        # reservation.status = 'annulee'
        # reservation.save()
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
                ['lacapacitee@gmail.com', settings.EMAIL_HOST_USER],
                fail_silently=False,
            )
            return render(request, 'users/contact_success.html')
    else:
        form = ContactForm()
    return render(request, 'users/contactUs.html', {'form': form})



def stripeHome(request):
    return render(request, 'users/paiement/stripe_home.html')


#stripe intégration
stripe.api_key=settings.STRIPE_SECRET_KEY

def checkout(request):
    reservation_id = request.GET.get('reservation_id')
    if not reservation_id:
        # return JsonResponse({'error': 'Reservation ID is missing'}, status=400)
        return JsonResponse({'error': "La réservation avec l'ID spécifié n'existe pas."}, status=400)

    try:
        reservation = Reservation.objects.get(id=reservation_id)
    except Reservation.DoesNotExist:
        return JsonResponse({'error': "La réservation n'existe pas."}, status=404)

    montant_reservation = reservation.prix_total  # Obtenez le montant du prix depuis votre modèle de réservation

    # Créez une session de paiement Stripe avec le montant du prix
    checkout_session_stripe = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'unit_amount': int(montant_reservation * 100),  # Convertissez le montant en cents pour Stripe
                'product_data': {
                    'name': 'Réservation',
                },
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url='http://localhost:8000/reservation/payment/success/',
        cancel_url='http://localhost:8000/cancel/',
    )

    # Redirigez l'utilisateur vers la page de paiement Stripe
    return redirect(checkout_session_stripe.url, code=303)

def stripe_confirm_payment(request):
    if request.method == 'POST':
        payment_intent_id = request.POST.get('payment_intent_id')
        reservation_id = request.POST.get('reservation_id')

        try:
            reservation = Reservation.objects.get(id=reservation_id)
        except Reservation.DoesNotExist:
            return JsonResponse({'error': "La réservation avec l'ID spécifié n'existe pas."}, status=404)

        if payment_intent_id:
            # Paiement Stripe réussi
            current_time = timezone.now()
            time_difference = current_time - reservation.date_creation
            time_difference_minutes = time_difference.total_seconds() / 60

            if time_difference_minutes <= 15:
                # Pendant les 15 premières minutes
                reservation.status = 'en_attente'
                reservation.bienloue.etat = 'en_cours'
            else:
                # Après 15 minutes
                reservation.status = 'validee'
                reservation.bienloue.etat = 'deja_reserve'

            reservation.paiement_effectue = True
            reservation.save()
            reservation.bienloue.save()

            return JsonResponse({'success': True})
        else:
            # Paiement Stripe échoué
            reservation.status = 'annulee'
            reservation.bienloue.etat = 'disponible'
            reservation.paiement_effectue = False
            reservation.save()
            reservation.bienloue.save()

            return JsonResponse({'error': "Le paiement Stripe a échoué."}, status=400)
    else:
        # Requête non autorisée
        return JsonResponse({'error': "Méthode de requête non autorisée."}, status=405)



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
            reservation.bienloue.etat = 'en_cours'
            reservation.bienloue.save()

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


@login_required
def process_payment(request, reservation_id):
    reservation = Reservation.objects.get(id=reservation_id)

    if reservation.is_payment_expired():
        # Paiement expiré, remettre l'état du bien à disponible
        reservation.bienloue.etat = 'disponible'
        reservation.bienloue.save()
        reservation.status = 'annulee'
        reservation.save()
        return render(request, 'users/payment_expired.html')

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
            "return_url": request.build_absolute_uri(
                reverse('execute_payment') + '?reservation_id=' + str(reservation_id)),
            "cancel_url": request.build_absolute_uri(
                reverse('cancel_payment') + '?reservation_id=' + str(reservation_id))
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
    payment_success = True  # Supposons que le paiement a réussi pour l'instant

    if payment_success:
        # Mettre à jour l'état du bien en 'deja_reserve' si le paiement a été effectué avec succès
        reservation.bienloue.etat = 'deja_reserve'
        reservation.bienloue.save()
        # Mettre à jour le statut de la réservation en 'validee' si le paiement a été effectué avec succès
        reservation.status = 'validee'
    else:
        # Mettre à jour l'état du bien en 'disponible' si le paiement a échoué ou a été annulé
        reservation.bienloue.etat = 'disponible'
        reservation.bienloue.save()
        # Mettre à jour le statut de la réservation en 'annulee' si le paiement a échoué ou a été annulé
        reservation.status = 'annulee'

    reservation.save()

    return redirect('payment_success')  # Redirection vers une page par défaut



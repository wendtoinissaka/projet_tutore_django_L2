from celery import shared_task
from django.utils import timezone
from .models import Reservation, Biens


@shared_task
def update_bien_state(bien_id):
    bien = Biens.objects.get(id=bien_id)
    reservations = Reservation.objects.filter(bienloue=bien, status='validee')

    # Vérifier s'il y a une réservation en cours
    if reservations.exists():
        reservation = reservations.first()
        if reservation.is_payment_expired():
            # Si le paiement a expiré, remettre l'état du bien à disponible
            bien.etat = 'disponible'
            bien.save()
        else:
            # Si le paiement est toujours valide, mettre à jour l'état du bien à deja_reserve
            bien.etat = 'deja_reserve'
            bien.save()

            # Planifier la réinitialisation de l'état du bien après la durée de la réservation
            nombre_jours = reservation.nombre_jours
            nouvelle_date = timezone.now() + timezone.timedelta(days=nombre_jours)
            bien.date_disponibilite_debut = nouvelle_date  # Mettre à jour la date du bien
            bien.date_disponibilite_fin = nouvelle_date  # Mettre à jour la date du bien
            bien.save()  # Sauvegarder les modifications sur le bien
            update_bien_state.apply_async((bien_id,), countdown=nombre_jours * 24 * 60 * 60)


# from datetime import timedelta
#
# from celery import shared_task
# from django.utils import timezone
# from .models import Reservation, Biens
#
# # Tâche pour mettre à jour l'état du bien si la réservation est expirée et le paiement n'a pas été effectué
# @shared_task
# def update_bien_state(reservation_id):
#     reservation = Reservation.objects.get(id=reservation_id)
#     bien = reservation.bienloue
#
#     # Vérifier si la réservation est expirée et le paiement n'a pas été effectué
#     if timezone.now() > reservation.date_expiration_paiement and reservation.statut != 'validee':
#         bien.etat = 'disponible'
#         bien.save()
#
#
# # from django.utils import timezone
# # from celery import shared_task
# # from .models import Reservation, Biens
# #
# #
# # @shared_task
# # def update_bien_state(bien_id):
# #     bien = Biens.objects.get(id=bien_id)
# #     try:
# #         # Récupérer la réservation en cours pour ce bien
# #         reservation = Reservation.objects.get(bienloue=bien, status='validee')
# #         # Vérifier si la durée de réservation est dépassée
# #         if reservation.date_expiration_paiement < timezone.now():
# #             bien.etat = 'disponible'  # Mettre le bien à nouveau disponible
# #         else:
# #             bien.etat = 'deja_reserve'  # Mettre le bien en état de réservation
# #         bien.save()
# #     except Reservation.DoesNotExist:
# #         # Aucune réservation valide n'a été trouvée pour ce bien
# #         bien.etat = 'disponible'  # Mettre le bien à nouveau disponible
# #         bien.save()

from datetime import timedelta

from celery import shared_task
from django.utils import timezone
from .models import Reservation, Biens

# Tâche pour mettre à jour l'état du bien si la réservation est expirée et le paiement n'a pas été effectué
@shared_task
def update_bien_state(reservation_id):
    reservation = Reservation.objects.get(id=reservation_id)
    bien = reservation.bienloue

    # Vérifier si la réservation est expirée et le paiement n'a pas été effectué
    if timezone.now() > reservation.date_expiration_paiement and reservation.statut != 'validee':
        bien.etat = 'disponible'
        bien.save()


# from django.utils import timezone
# from celery import shared_task
# from .models import Reservation, Biens
#
#
# @shared_task
# def update_bien_state(bien_id):
#     bien = Biens.objects.get(id=bien_id)
#     try:
#         # Récupérer la réservation en cours pour ce bien
#         reservation = Reservation.objects.get(bienloue=bien, status='validee')
#         # Vérifier si la durée de réservation est dépassée
#         if reservation.date_expiration_paiement < timezone.now():
#             bien.etat = 'disponible'  # Mettre le bien à nouveau disponible
#         else:
#             bien.etat = 'deja_reserve'  # Mettre le bien en état de réservation
#         bien.save()
#     except Reservation.DoesNotExist:
#         # Aucune réservation valide n'a été trouvée pour ce bien
#         bien.etat = 'disponible'  # Mettre le bien à nouveau disponible
#         bien.save()

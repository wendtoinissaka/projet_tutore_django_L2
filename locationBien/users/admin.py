from django.contrib import admin
from .models import Biens, Avis, Reservation

@admin.register(Biens)
class BiensAdmin(admin.ModelAdmin):
    list_display = ('nom', 'proprietaire', 'categories', 'localisation', 'prix')
    search_fields = ('nom', 'localisation')

@admin.register(Avis)
class AvisAdmin(admin.ModelAdmin):
    list_display = ('bien', 'locataire', 'note', 'commentaire')
    search_fields = ('bien__nom', 'locataire__username')

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('bienloue', 'locataire', 'proprietaire', 'status', 'prix', 'datereservation')
    list_filter = ('status',)
    search_fields = ('bienloue__nom', 'locataire__username', 'proprietaire__username')




# from django.contrib import admin
# from django.contrib.auth.models import User
# from .models import Biens
#
# # Définir la classe d'administration pour le modèle Biens
# class BiensAdmin(admin.ModelAdmin):
#     list_display = ('nom', 'categories', 'proprietaire', 'localisation', 'prix')  # Les champs à afficher dans la liste d'administration
#
# # Enregistrer le modèle Biens dans l'interface d'administration avec sa classe d'administration
# admin.site.register(Biens, BiensAdmin)
#
# # Désenregistrer la classe d'administration par défaut pour le modèle User
# admin.site.unregister(User)
#
# # Définir une classe d'administration personnalisée pour le modèle User
# class UtilisateurAdmin(admin.ModelAdmin):
#     list_display = ('username', 'email', 'is_active', 'date_joined')  # Exemple de champs à afficher dans la liste d'administration
#
# # Enregistrer le modèle User avec la classe d'administration personnalisée
# admin.site.register(User, UtilisateurAdmin)

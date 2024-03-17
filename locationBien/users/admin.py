from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Biens, Avis, Reservation, CustomUser

# Créez une classe d'administration personnalisée pour votre modèle CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    # model = CustomUser
    list_display = ('username', 'email', 'nom', 'type', 'numero_tel')  # Ajoutez les champs que vous souhaitez afficher dans l'interface d'administration
    search_fields = ('username', 'email', 'nom', 'type')  # Ajoutez les champs que vous souhaitez inclure dans la recherche
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('email', 'nom', 'numero_tel', 'type')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'nom', 'numero_tel', 'type'),
        }),
    )

# Enregistrez votre modèle CustomUser avec la classe d'administration personnalisée
# admin.site.register(CustomUser, CustomUserAdmin)

# Enregistrez vos autres modèles
# @admin.register(Biens)
# class BiensAdmin(admin.ModelAdmin):
#     list_display = ('nom', 'proprietaire', 'categories', 'localisation', 'prix', 'etat')
#     search_fields = ('nom', 'localisation')


@admin.register(Biens)
class BiensAdmin(admin.ModelAdmin):
    list_display = ('nom', 'proprietaire', 'categories', 'localisation', 'prix', 'etat')
    search_fields = ('nom', 'localisation')
    list_filter = ('etat',)  # Ajoutez cette ligne pour ajouter le filtre par état




@admin.register(Avis)
class AvisAdmin(admin.ModelAdmin):
    list_display = ('bien', 'locataire', 'note', 'commentaire')
    search_fields = ('bien__nom', 'locataire__username')


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('bienloue', 'locataire', 'proprietaire', 'status', 'datereservation')
    list_filter = ('status',)
    search_fields = ('bienloue__nom', 'locataire__username', 'proprietaire__username')

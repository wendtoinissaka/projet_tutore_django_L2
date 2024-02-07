from django.db import models
from django.contrib.auth.models import User

class Biens(models.Model):
    CATEGORIES_CHOICES = (
        ('immobilier', 'Immobilier'),
        ('vehicule', 'Véhicule'),
        ('equipements', 'Équipements'),
        ('autres', 'Autres'),
    )

    proprietaire = models.ForeignKey(User, on_delete=models.CASCADE)
    nom = models.CharField(max_length=100)
    categories = models.CharField(max_length=20, choices=CATEGORIES_CHOICES)
    localisation = models.CharField(max_length=255)
    description = models.TextField()
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    photos = models.ImageField(upload_to='biens_photos/')

    def __str__(self):
        return self.nom

class Avis(models.Model):
    note = models.IntegerField()
    commentaire = models.TextField()
    bien = models.ForeignKey(Biens, on_delete=models.CASCADE)
    locataire = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Avis sur {self.bien.nom} par {self.locataire.username}"

class Reservation(models.Model):
    STATUS_CHOICES = (
        ('en_attente', 'En attente'),
        ('validee', 'Validée'),
        ('annulee', 'Annulée'),
    )

    datereservation = models.DateTimeField(auto_now_add=True)
    bienloue = models.ForeignKey(Biens, on_delete=models.CASCADE)
    locataire = models.ForeignKey(User, on_delete=models.CASCADE)
    proprietaire = models.ForeignKey(User, related_name='reservations_recues', on_delete=models.CASCADE)
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    def __str__(self):
        return f"Réservation de {self.bienloue.nom} par {self.locataire.username}, statut: {self.status}"



# from django.contrib.auth.models import User
# from django.db import models
#
# class Biens(models.Model):
#     CATEGORIES_CHOICES = (
#         ('immobilier', 'Immobilier'),
#         ('vehicule', 'Véhicule'),
#         ('equipements', 'Équipements'),
#         ('autres', 'Autres'),
#     )
#
#     proprietaire = models.ForeignKey(User, on_delete=models.CASCADE)
#     nom = models.CharField(max_length=100)
#     categories = models.CharField(max_length=20, choices=CATEGORIES_CHOICES)
#     localisation = models.CharField(max_length=255)
#     description = models.TextField()
#     prix = models.DecimalField(max_digits=10, decimal_places=2)
#     photos = models.ImageField(upload_to='biens_photos/')
#
#     def __str__(self):
#         return self.nom
#
#     class Biens(models.Model):
#         CATEGORIES_CHOICES = (
#             ('immobilier', 'Immobilier'),
#             ('vehicule', 'Véhicule'),
#             ('equipements', 'Équipements'),
#             ('autres', 'Autres'),
#         )
#
#         proprietaire = models.ForeignKey(User, on_delete=models.CASCADE)
#         nom = models.CharField(max_length=100)
#         categories = models.CharField(max_length=20, choices=CATEGORIES_CHOICES)
#         localisation = models.CharField(max_length=255)
#         description = models.TextField()
#         prix = models.DecimalField(max_digits=10, decimal_places=2)
#         photos = models.ImageField(upload_to='biens_photos/')
#
#         def __str__(self):
#             return self.nom
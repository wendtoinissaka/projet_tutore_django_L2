from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth.models import User


class Biens(models.Model):
    CATEGORIES_CHOICES = (
        ('immobilier', 'Immobilier'),
        ('vehicule', 'Véhicule'),
        ('equipements', 'Équipements'),
        ('autres', 'Autres'),
    )

    ETAT_CHOICES = (
        ('disponible', 'Disponible'),
        ('non_disponible', 'Non disponible'),
    )

    proprietaire = models.ForeignKey(User, on_delete=models.CASCADE)
    nom = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)
    categories = models.CharField(max_length=20, choices=CATEGORIES_CHOICES)
    localisation = models.CharField(max_length=255)
    description = models.TextField()
    prix = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])  # Prix non négatif
    image_principale = models.ImageField(upload_to='biens_photos/')  # Image principale obligatoire
    image_facultative_1 = models.ImageField(upload_to='biens_photos/', blank=True, null=True)  # Image facultative 1
    image_facultative_2 = models.ImageField(upload_to='biens_photos/', blank=True, null=True)  # Image facultative 2
    image_facultative_3 = models.ImageField(upload_to='biens_photos/', blank=True, null=True)  # Image facultative 3
    image_facultative_4 = models.ImageField(upload_to='biens_photos/', blank=True, null=True)  # Image facultative 4
    etat = models.CharField(max_length=20, choices=ETAT_CHOICES,
                            default='disponible')  # Etat du bien (disponible par défaut)

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
    prix = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])  # Prix non négatif
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='en_attente')

    def __str__(self):
        return f"Réservation de {self.bienloue.nom} par {self.locataire.username}, statut: {self.status}"






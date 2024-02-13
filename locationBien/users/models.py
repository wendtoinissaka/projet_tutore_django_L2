from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth.models import User, AbstractUser

class CustomUser(AbstractUser):
    TYPES_USERS = (
        ('locataire', 'Locataire'),
        ('proprietaire', 'Propriétaire'),
        ('administrateur', 'Administrateur'),
    )
    nom = models.CharField(max_length=100)
    numero_tel = models.CharField(max_length=15)
    email = models.EmailField(unique=True)  # Ajout du champ email
    type = models.CharField(max_length=20,choices=TYPES_USERS, default='locataire')  # Par défaut, type = 'locataire'
    # Ajout des related_names pour résoudre les conflits
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',  # Nouveau related_name pour éviter le conflit
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',  # Nouveau related_name pour éviter le conflit
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.',
    )

    def __str__(self):
        return self.username

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

    proprietaire = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
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
    etat = models.CharField(max_length=20, choices=ETAT_CHOICES,
                            default='disponible')  # Etat du bien (disponible par défaut)

    def __str__(self):
        return self.nom

# class Avis(models.Model):
#     note = models.IntegerField()
#     commentaire = models.TextField()
#     bien = models.ForeignKey(Biens, on_delete=models.CASCADE)
#     locataire = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

class Avis(models.Model):
    NOTE_CHOICES = [(i, f'{"⭐"*i}') for i in range(1, 6)]

    bien = models.ForeignKey(Biens, related_name='avis', on_delete=models.CASCADE)
    locataire = models.ForeignKey(CustomUser, related_name='avis', on_delete=models.CASCADE)
    note = models.PositiveSmallIntegerField(choices=NOTE_CHOICES)
    commentaire = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.note}/5 par {self.locataire} sur {self.bien}'




# class Avis(models.Model):
#     note = models.IntegerField()
#     commentaire = models.TextField()
#     bien = models.ForeignKey(Biens, on_delete=models.CASCADE)
#     locataire = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#
#     def __str__(self):
#         return f"Avis sur {self.bien.nom} par {self.locataire.username}"


class Reservation(models.Model):
    STATUS_CHOICES = (
        ('en_attente', 'En attente'),
        ('validee', 'Validée'),
        ('annulee', 'Annulée'),
    )

    datereservation = models.DateTimeField(auto_now_add=True)
    bienloue = models.ForeignKey(Biens, on_delete=models.CASCADE)
    locataire = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    proprietaire = models.ForeignKey(CustomUser, related_name='reservations_recues', on_delete=models.CASCADE)
    prix = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])  # Prix non négatif
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='en_attente')

    def __str__(self):
        return f"Réservation de {self.bienloue.nom} par {self.locataire.username}, statut: {self.status}"






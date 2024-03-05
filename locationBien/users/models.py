from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.utils import timezone
from django.contrib.auth.tokens import default_token_generator


class CustomUser(AbstractUser):
    TYPES_USERS = (
        ('locataire', 'Locataire'),
        ('proprietaire', 'Propriétaire'),
        ('administrateur', 'Administrateur'),
    )
    is_active = models.BooleanField(default=False)
    # is_admin = models.BooleanField(default=True)
    nom = models.CharField(max_length=100)
    numero_tel = models.CharField(max_length=15)
    email = models.EmailField(unique=True)  # Ajout du champ emails
    type = models.CharField(max_length=20, choices=TYPES_USERS, default='locataire')  # Par défaut, type = 'locataire'
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

    def generate_activation_token(self):
        """
        Génère un nouveau token d'activation pour l'utilisateur.
        """
        return default_token_generator.make_token(self)

    def __str__(self):
        return self.username






class Biens(models.Model):
    date_disponibilite_debut = models.DateTimeField(null=True, blank=True)
    date_disponibilite_fin = models.DateTimeField(null=True, blank=True)

    def update_state(self):
        reservations = self.reservation_set.filter(status='validee', paiement_effectue=True)
        now = timezone.now()

        # Update bien state based on reservations
        for reservation in reservations:
            if reservation.date_expiration_paiement > now:
                # Reservation payment not expired, bien is 'en_cours'
                self.etat = 'en_cours'
            else:
                # Reservation payment expired, bien is 'disponible'
                self.etat = 'disponible'

        self.save()

    def is_available(self):
        return self.date_disponibilite_debut is None or self.date_disponibilite_fin is None

    def get_reservation_price(self, num_days):
        if not self.is_available():
            return None
        return self.prix * num_days

    def get_related_biens(self):
        return Biens.objects.filter(categories=self.categories).exclude(id=self.id)[:8]

    CATEGORIES_CHOICES = (
        ('immobiliers', 'Immobiliers'),
        ('vehicules', 'Véhicules'),
        ('equipements', 'Équipements'),
        ('services', 'Services'),
        ('autres', 'Autres'),
    )

    ETAT_CHOICES = (
        ('disponible', 'Disponible'),
        ('deja_reserve', 'deja reserve'),
        ('en_cours', 'En cours'),
    )

    proprietaire = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    # nom = models.CharField(max_length=100)
    nom = models.CharField(max_length=50)
    date_created = models.DateTimeField(auto_now_add=True)
    categories = models.CharField(max_length=20, choices=CATEGORIES_CHOICES)
    localisation = models.CharField(max_length=255)
    description = models.TextField()
    prix = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    # image_principale = models.ImageField(upload_to='biens_photos/')
    image_principale = models.ImageField(upload_to='biens_photos/')
    # image_principale = models.ImageField(upload_to='biens_photos/', default='users/images/bg44.jpg')
    image_facultative_1 = models.ImageField(upload_to='biens_photos/', blank=True, null=True)
    image_facultative_2 = models.ImageField(upload_to='biens_photos/', blank=True, null=True)
    image_facultative_3 = models.ImageField(upload_to='biens_photos/', blank=True, null=True)
    etat = models.CharField(max_length=20, choices=ETAT_CHOICES, default='disponible')
    # date_modification = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.date_modification = timezone.now()

        # Convertir le nom en majuscules avant l'enregistrement
        self.nom = self.nom.upper()
        super(Biens, self).save(*args, **kwargs)

    def __str__(self):
        return self.nom

    def get_time_remaining(self):
        now = timezone.now()
        if self.date_disponibilite_fin and now < self.date_disponibilite_fin:
            time_difference = self.date_disponibilite_fin - now
            return time_difference
        return None

    def get_time_until_available(self):
        if self.etat == 'deja_reserve':
            now = timezone.now()
            if self.date_disponibilite_fin and now < self.date_disponibilite_fin:
                time_difference = self.date_disponibilite_fin - now
                hours, remainder = divmod(time_difference.seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                return f"{hours} heures, {minutes} minutes, {seconds} secondes"
        return None



class Reservation(models.Model):
    nombre_jours = models.PositiveIntegerField(default=1)
    debut_reservation = models.DateField()
    fin_reservation = models.DateField()
    prix_total = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], null=True)
    paiement_effectue = models.BooleanField(default=False)
    date_expiration_paiement = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        bien = self.bienloue
        prix_reservation = bien.get_reservation_price(self.nombre_jours)
        if prix_reservation:
            self.prix_total = prix_reservation
            bien.date_disponibilite_debut = None
            bien.date_disponibilite_fin = None
            bien.save()
        # Définir l'heure d'expiration du paiement (30 minutes après la création de la réservation)
        if not self.date_expiration_paiement:
            self.date_expiration_paiement = timezone.now() + timezone.timedelta(minutes=15)
            # self.date_expiration_paiement = timezone.now() + timezone.timedelta(minutes=30)
            # self.date_expiration_paiement = timezone.now() + timezone.timedelta(heures=1)

        super().save(*args, **kwargs)

    STATUS_CHOICES = (
        ('en_attente', 'En attente'),
        ('validee', 'Validée'),
        ('annulee', 'Annulée'),
    )

    datereservation = models.DateTimeField(auto_now_add=True)
    bienloue = models.ForeignKey(Biens, on_delete=models.CASCADE)
    locataire = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    proprietaire = models.ForeignKey(CustomUser, related_name='reservations_recues', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='en_attente')

    def is_payment_expired(self):
        return timezone.now() > self.date_expiration_paiement

    def __str__(self):
        return f"Réservation de {self.bienloue.nom} par {self.locataire.username}, statut: {self.status}"


class Avis(models.Model):
    NOTE_CHOICES = [(i, f'{"⭐" * i}') for i in range(1, 6)]

    bien = models.ForeignKey(Biens, related_name='avis', on_delete=models.CASCADE)
    locataire = models.ForeignKey(CustomUser, related_name='avis', on_delete=models.CASCADE)
    note = models.PositiveSmallIntegerField(choices=NOTE_CHOICES)
    commentaire = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.note}/5 par {self.locataire} sur {self.bien}'


User = get_user_model()


class Payment(models.Model):
    STATUT_CHOICES = (
        ('en_attente', 'En attente'),
        ('validee', 'Validée'),
        ('annulee', 'Annulée'),
    )

    bien = models.ForeignKey(Biens, on_delete=models.CASCADE)
    locataire = models.ForeignKey(User, on_delete=models.CASCADE)
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    date_paiement = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')

    def __str__(self):
        return f"Paiement de {self.montant} pour {self.bien.nom} par {self.locataire.username}, statut: {self.statut}"

# Generated by Django 5.0.1 on 2024-03-05 17:06

import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('is_active', models.BooleanField(default=False)),
                ('nom', models.CharField(max_length=100)),
                ('numero_tel', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('type', models.CharField(choices=[('locataire', 'Locataire'), ('proprietaire', 'Propriétaire'), ('administrateur', 'Administrateur')], default='locataire', max_length=20)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='customuser_set', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='customuser_set', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Biens',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_disponibilite_debut', models.DateTimeField(blank=True, null=True)),
                ('date_disponibilite_fin', models.DateTimeField(blank=True, null=True)),
                ('nom', models.CharField(max_length=50)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('categories', models.CharField(choices=[('immobiliers', 'Immobiliers'), ('vehicules', 'Véhicules'), ('equipements', 'Équipements'), ('services', 'Services'), ('autres', 'Autres')], max_length=20)),
                ('localisation', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('prix', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('image_principale', models.ImageField(upload_to='biens_photos/')),
                ('image_facultative_1', models.ImageField(blank=True, null=True, upload_to='biens_photos/')),
                ('image_facultative_2', models.ImageField(blank=True, null=True, upload_to='biens_photos/')),
                ('image_facultative_3', models.ImageField(blank=True, null=True, upload_to='biens_photos/')),
                ('etat', models.CharField(choices=[('disponible', 'Disponible'), ('deja_reserve', 'deja reserve'), ('en_cours', 'En cours')], default='disponible', max_length=20)),
                ('date_modification', models.DateTimeField(auto_now=True)),
                ('proprietaire', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Avis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note', models.PositiveSmallIntegerField(choices=[(1, '⭐'), (2, '⭐⭐'), (3, '⭐⭐⭐'), (4, '⭐⭐⭐⭐'), (5, '⭐⭐⭐⭐⭐')])),
                ('commentaire', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('locataire', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='avis', to=settings.AUTH_USER_MODEL)),
                ('bien', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='avis', to='users.biens')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('montant', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date_paiement', models.DateTimeField(auto_now_add=True)),
                ('statut', models.CharField(choices=[('en_attente', 'En attente'), ('validee', 'Validée'), ('annulee', 'Annulée')], default='en_attente', max_length=20)),
                ('bien', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.biens')),
                ('locataire', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_jours', models.PositiveIntegerField(default=1)),
                ('debut_reservation', models.DateField()),
                ('fin_reservation', models.DateField()),
                ('prix_total', models.DecimalField(decimal_places=2, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('paiement_effectue', models.BooleanField(default=False)),
                ('date_expiration_paiement', models.DateTimeField(blank=True, null=True)),
                ('datereservation', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('en_attente', 'En attente'), ('validee', 'Validée'), ('annulee', 'Annulée')], default='en_attente', max_length=20)),
                ('bienloue', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.biens')),
                ('locataire', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('proprietaire', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservations_recues', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

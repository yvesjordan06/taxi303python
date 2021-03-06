# Generated by Django 3.0.2 on 2020-01-23 00:48

import django.core.validators
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Utilisateur',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False,
                                                     help_text='Designates that this user has all permissions without explicitly assigning them.',
                                                     verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False,
                                                 help_text='Designates whether the user can log into this admin site.',
                                                 verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True,
                                                  help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.',
                                                  verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('code', models.CharField(max_length=64)),
                ('telephone', models.CharField(max_length=64, unique=True)),
                ('cni', models.CharField(max_length=64, unique=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True,
                                                  help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
                                                  related_name='user_set', related_query_name='user', to='auth.Group',
                                                  verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.',
                                                            related_name='user_set', related_query_name='user',
                                                            to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                (
                'user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Colis',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(
                    choices=[('YDE', 'Yaounde'), ('DLA', 'Douala'), ('BAF', 'Baffoussam'), ('BDA', 'Bamenda'),
                             ('BDJ', 'Bandjoun')], max_length=64)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='taxi.Client')),
            ],
        ),
        migrations.CreateModel(
            name='Employe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('salaire', models.BigIntegerField(default='50000')),
                ('poste', models.CharField(choices=[('CHAUFFEUR', 'Chauffeur'), ('GUICHETIER', 'Guichetier')],
                                           default='CHAUFFEUR', max_length=32)),
                (
                'user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Programme',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('depart', models.CharField(
                    choices=[('YDE', 'Yaounde'), ('DLA', 'Douala'), ('BAF', 'Baffoussam'), ('BDA', 'Bamenda'),
                             ('BDJ', 'Bandjoun')], max_length=64)),
                ('arrive', models.CharField(
                    choices=[('YDE', 'Yaounde'), ('DLA', 'Douala'), ('BAF', 'Baffoussam'), ('BDA', 'Bamenda'),
                             ('BDJ', 'Bandjoun')], max_length=64)),
                ('type', models.CharField(choices=[('CL', 'Classique'), ('VIP', 'VIP')], default='CL', max_length=64)),
                ('heure_depart', models.CharField(choices=[('CL', 'Classique'), ('VIP', 'VIP')], max_length=64)),
                ('tarif', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Voiture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('marque', models.CharField(max_length=64)),
                ('categorie', models.CharField(max_length=64)),
                ('matricule', models.CharField(max_length=8)),
                ('places', models.IntegerField(default=70)),
                ('places_occuper', models.IntegerField(default=0)),
                ('chauffeur', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                                                   to='taxi.Employe')),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('places', models.IntegerField(default=1, validators=[django.core.validators.MaxValueValidator(5),
                                                                      django.core.validators.MinValueValidator(1)])),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Created at')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='taxi.Client')),
                ('programme', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='taxi.Programme')),
            ],
        ),
        migrations.AddField(
            model_name='programme',
            name='voiture',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                                    to='taxi.Voiture'),
        ),
        migrations.CreateModel(
            name='Expedition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('depart', models.CharField(
                    choices=[('YDE', 'Yaounde'), ('DLA', 'Douala'), ('BAF', 'Baffoussam'), ('BDA', 'Bamenda'),
                             ('BDJ', 'Bandjoun')], max_length=64)),
                ('arrive', models.CharField(
                    choices=[('YDE', 'Yaounde'), ('DLA', 'Douala'), ('BAF', 'Baffoussam'), ('BDA', 'Bamenda'),
                             ('BDJ', 'Bandjoun')], max_length=64)),
                ('tarif', models.IntegerField()),
                ('livree', models.BooleanField(default=False)),
                ('colis', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='taxi.Colis')),
            ],
        ),
    ]

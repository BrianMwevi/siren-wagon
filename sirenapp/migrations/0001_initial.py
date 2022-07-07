# Generated by Django 4.0.5 on 2022-07-07 07:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ambulance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_plate', models.CharField(blank=True, max_length=200, null=True)),
                ('available', models.BooleanField(default=False, verbose_name='available')),
            ],
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=55)),
                ('last_name', models.CharField(max_length=55)),
                ('email', models.EmailField(max_length=255)),
                ('phone', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Package',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('package_choice', models.CharField(choices=[('1', 'Regular'), ('2', 'Premium')], default='regular', max_length=200)),
                ('amount', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveIntegerField(default=0)),
                ('transaction_type', models.CharField(max_length=55)),
                ('completed', models.BooleanField(default=False)),
                ('transaction_date', models.DateTimeField(auto_now_add=True)),
                ('sender', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sender', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pickup', models.CharField(max_length=255)),
                ('persons', models.PositiveIntegerField(default=3)),
                ('trip_date', models.DateTimeField(auto_now_add=True)),
                ('completed', models.BooleanField(default=False)),
                ('fee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='trip_fee', to='sirenapp.transaction')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(blank=True, null=True)),
                ('rating', models.PositiveIntegerField(default=1)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviewer', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Hospital',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('location', models.CharField(max_length=255)),
                ('established_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('ambulances', models.ManyToManyField(blank=True, related_name='hospital_ambulances', to='sirenapp.ambulance')),
                ('doctors', models.ManyToManyField(blank=True, related_name='hospital_doctors', to='sirenapp.doctor')),
                ('patients', models.ManyToManyField(blank=True, related_name='hospital_patients', to=settings.AUTH_USER_MODEL)),
                ('reviews', models.ManyToManyField(blank=True, related_name='hospital_reviews', to='sirenapp.review')),
            ],
        ),
        migrations.CreateModel(
            name='Driver',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=55)),
                ('last_name', models.CharField(max_length=55)),
                ('email', models.EmailField(max_length=255)),
                ('phone', models.CharField(max_length=255)),
                ('trips', models.ManyToManyField(blank=True, related_name='trips', to='sirenapp.trip')),
            ],
        ),
        migrations.CreateModel(
            name='CustomerAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_number', models.PositiveBigIntegerField(blank=True, null=True, unique=True)),
                ('balance', models.PositiveIntegerField(default=0)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('hospital', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='hospital_account', to='sirenapp.hospital')),
            ],
        ),
        migrations.AddField(
            model_name='ambulance',
            name='ratings',
            field=models.ManyToManyField(blank=True, related_name='ratings', to='sirenapp.review'),
        ),
        migrations.AddField(
            model_name='ambulance',
            name='trips',
            field=models.ManyToManyField(blank=True, related_name='ambulance_trips', to='sirenapp.trip'),
        ),
    ]

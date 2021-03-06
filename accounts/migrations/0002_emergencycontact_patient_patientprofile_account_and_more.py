# Generated by Django 4.0.5 on 2022-07-07 07:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sirenapp', '0002_ambulance_driver_customeraccount_account_holder_and_more'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='emergencycontact',
            name='patient',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='patient_emergency', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='patientprofile',
            name='account',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='patient_account', to='sirenapp.customeraccount'),
        ),
        migrations.AddField(
            model_name='patientprofile',
            name='package',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='patient_packages', to='sirenapp.package'),
        ),
        migrations.AddField(
            model_name='user',
            name='account',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='account', to='sirenapp.customeraccount'),
        ),
    ]

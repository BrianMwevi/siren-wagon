# Generated by Django 4.0.5 on 2022-07-06 09:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sirenapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='ambulance',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ambulance_reviews', to='sirenapp.ambulance'),
        ),
        migrations.AddField(
            model_name='trip',
            name='fee',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='trip_fee', to='sirenapp.transaction'),
        ),
    ]
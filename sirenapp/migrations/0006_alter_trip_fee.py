# Generated by Django 4.0.5 on 2022-07-05 06:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sirenapp', '0005_alter_package_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trip',
            name='fee',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='trip_fee', to='sirenapp.transaction'),
        ),
    ]

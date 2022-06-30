# Generated by Django 4.0.5 on 2022-06-30 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sirenapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='trip',
            name='destination',
            field=models.CharField(default='Kilimani', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='trip',
            name='pickup',
            field=models.CharField(default='Junction', max_length=255),
            preserve_default=False,
        ),
    ]

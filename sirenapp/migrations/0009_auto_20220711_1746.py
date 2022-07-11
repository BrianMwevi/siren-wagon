# Generated by Django 3.2 on 2022-07-11 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sirenapp', '0008_auto_20220711_1743'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ambulance',
            name='phone',
            field=models.PositiveBigIntegerField(unique=True),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='phone',
            field=models.PositiveBigIntegerField(unique=True),
        ),
        migrations.AlterField(
            model_name='hospital',
            name='phone',
            field=models.PositiveBigIntegerField(unique=True),
        ),
    ]
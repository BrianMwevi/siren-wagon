# Generated by Django 3.2 on 2022-07-11 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sirenapp', '0004_auto_20220711_1630'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ambulance',
            name='phone',
            field=models.PositiveBigIntegerField(),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='phone',
            field=models.PositiveBigIntegerField(),
        ),
        migrations.AlterField(
            model_name='hospital',
            name='phone',
            field=models.PositiveBigIntegerField(),
        ),
    ]

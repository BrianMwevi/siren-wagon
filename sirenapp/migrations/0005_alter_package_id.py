# Generated by Django 4.0.5 on 2022-07-04 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sirenapp', '0004_alter_package_id_alter_package_package_choice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='package',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
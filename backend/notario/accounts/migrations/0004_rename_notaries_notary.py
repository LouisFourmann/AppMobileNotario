# Generated by Django 4.1.4 on 2022-12-12 14:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_user_age_user_phone'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Notaries',
            new_name='Notary',
        ),
    ]
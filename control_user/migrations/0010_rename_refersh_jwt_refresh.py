# Generated by Django 4.0.6 on 2022-08-18 00:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('control_user', '0009_customuser_first_name_customuser_last_name_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='jwt',
            old_name='refersh',
            new_name='refresh',
        ),
    ]

# Generated by Django 4.0.6 on 2022-08-17 00:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_user', '0007_alter_customuser_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='caption',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='first_name',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='last_name',
            field=models.CharField(max_length=100, null=True),
        ),
    ]

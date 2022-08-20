# Generated by Django 4.0.6 on 2022-08-17 01:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('message_control', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='genericfileupload',
            name='uploader',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='uploader_user', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
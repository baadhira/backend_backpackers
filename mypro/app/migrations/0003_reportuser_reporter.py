# Generated by Django 4.0.4 on 2022-05-26 04:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_reportuser_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='reportuser',
            name='reporter',
            field=models.ForeignKey(default=3, on_delete=django.db.models.deletion.CASCADE, related_name='reporter', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]

# Generated by Django 4.0.4 on 2022-06-08 05:47

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_delete_blockuser'),
    ]

    operations = [
        migrations.AddField(
            model_name='album',
            name='created_date',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]

# Generated by Django 4.0.4 on 2022-06-09 03:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_alter_album_created_date'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Album',
        ),
    ]

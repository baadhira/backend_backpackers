# Generated by Django 4.0.4 on 2022-06-10 11:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('discussion', '0018_comment'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Comment',
        ),
    ]

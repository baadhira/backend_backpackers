# Generated by Django 4.0.4 on 2022-05-09 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0008_alter_event_description_alter_event_enddate_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='events'),
        ),
    ]

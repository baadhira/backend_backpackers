# Generated by Django 4.0.4 on 2022-06-13 05:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discussion', '0021_reportcomment'),
    ]

    operations = [
        migrations.AddField(
            model_name='reportcomment',
            name='reason',
            field=models.CharField(choices=[("It's spam", "It's spam"), ('Hate speech or symbols', 'Hate speech or symbols'), ('Bullying or harassement', 'Bullying or harassement'), ('Nudity or sexual activity', 'Nudity or sexual activity')], default='dd', max_length=150),
            preserve_default=False,
        ),
    ]

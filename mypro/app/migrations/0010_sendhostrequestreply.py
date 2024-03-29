# Generated by Django 4.0.4 on 2022-06-01 12:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_reportuser_text_sendhostrequest_created_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='SendHostRequestReply',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('hostrequest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.sendhostrequest')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='replysender', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

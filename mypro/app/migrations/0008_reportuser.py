# Generated by Django 4.0.4 on 2022-05-30 12:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_blockuser_delete_reportuser'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReportUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.CharField(choices=[("It's posting content that shouldn't be here", "It's posting content that shouldn't be here"), ("It's pretending to be someone else", "It's pretending to be someone else")], max_length=150)),
                ('reporter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reporter', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users_reported', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

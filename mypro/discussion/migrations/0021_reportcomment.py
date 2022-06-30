# Generated by Django 4.0.4 on 2022-06-13 05:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('discussion', '0020_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReportComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now=True)),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reported_comment', to='discussion.comment')),
                ('reporter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_reporter', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
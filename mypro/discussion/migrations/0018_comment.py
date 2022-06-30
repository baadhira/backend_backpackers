# Generated by Django 4.0.4 on 2022-06-09 11:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('discussion', '0017_delete_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(max_length=250)),
                ('date', models.DateTimeField(auto_now=True)),
                ('from_discussion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_discussion', to='discussion.discussion')),
                ('parent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='reply_set', to='discussion.comment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='commenter', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
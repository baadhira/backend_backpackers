# Generated by Django 4.0.4 on 2022-05-13 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discussion', '0005_alter_discussion_createddate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discussioncomment',
            name='text',
            field=models.CharField(default='new', max_length=255),
            preserve_default=False,
        ),
    ]

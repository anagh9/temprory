# Generated by Django 4.1.1 on 2022-09-13 18:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_collection_genres'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='collection',
            name='genres',
        ),
    ]

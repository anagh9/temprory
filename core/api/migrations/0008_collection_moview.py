# Generated by Django 4.1.1 on 2022-09-13 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_collection_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='collection',
            name='moview',
            field=models.JSONField(default=1),
            preserve_default=False,
        ),
    ]
# Generated by Django 3.0 on 2019-12-18 11:39

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('fbbot', '0004_auto_20191218_1239'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='photo_url',
            field=models.URLField(max_length=400, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='url',
            field=models.URLField(max_length=400, null=True),
        ),
    ]

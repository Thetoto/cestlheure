# Generated by Django 3.0 on 2019-12-31 22:03

import django.contrib.postgres.fields.jsonb
from django.db import migrations
import fbbot.models


class Migration(migrations.Migration):
    dependencies = [
        ('fbbot', '0007_auto_20191231_2302'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='full_object',
            field=django.contrib.postgres.fields.jsonb.JSONField(encoder=django.core.serializers.json.DjangoJSONEncoder,
                                                                 null=True),
        ),
    ]

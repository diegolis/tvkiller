# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('thumbs', '0004_clip_thumb'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clip',
            name='filename',
            field=models.FileField(upload_to=b''),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='origin',
            name='filename',
            field=models.FileField(upload_to=b''),
            preserve_default=True,
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('thumbs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='thumb',
            name='filename',
            field=models.FileField(upload_to=b''),
            preserve_default=True,
        ),
    ]

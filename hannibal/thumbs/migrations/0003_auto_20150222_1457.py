# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('thumbs', '0002_auto_20150222_0050'),
    ]

    operations = [
        migrations.AddField(
            model_name='clip',
            name='hashid',
            field=models.CharField(default=None, unique=True, max_length=10, editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='clip',
            name='status',
            field=model_utils.fields.StatusField(default=b'in_process', max_length=100, no_check_for_status=True, choices=[(0, 'dummy')]),
            preserve_default=True,
        ),
    ]

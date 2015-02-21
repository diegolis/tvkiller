# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('thumbs', '0003_auto_20150221_2115'),
    ]

    operations = [
        migrations.CreateModel(
            name='Clip',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('filename', models.FileField(upload_to=b'')),
                ('channel', models.ForeignKey(to='thumbs.Channel')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='origin',
            name='filename',
            field=models.FileField(upload_to=b''),
            preserve_default=True,
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('population', '0009_supplydemand_population'),
    ]

    operations = [
        migrations.AddField(
            model_name='resource',
            name='name',
            field=models.TextField(default='a'),
            preserve_default=False,
        ),
    ]

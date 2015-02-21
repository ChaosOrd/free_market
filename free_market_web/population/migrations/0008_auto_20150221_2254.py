# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('population', '0007_supplydemand'),
    ]

    operations = [
        migrations.AddField(
            model_name='supplydemand',
            name='resource',
            field=models.ForeignKey(default=0, to='population.Resource'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='supplydemand',
            name='value',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]

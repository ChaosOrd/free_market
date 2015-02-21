# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('population', '0008_auto_20150221_2254'),
    ]

    operations = [
        migrations.AddField(
            model_name='supplydemand',
            name='population',
            field=models.ForeignKey(default=0, to='population.Population'),
            preserve_default=False,
        ),
    ]

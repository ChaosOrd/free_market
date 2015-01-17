# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('population', '0003_universe'),
    ]

    operations = [
        migrations.AddField(
            model_name='population',
            name='universe',
            field=models.ForeignKey(default=0, to='population.Universe'),
            preserve_default=False,
        ),
    ]

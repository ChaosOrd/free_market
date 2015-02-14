# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('population', '0004_population_universe'),
    ]

    operations = [
        migrations.AlterField(
            model_name='population',
            name='name',
            field=models.TextField(verbose_name='name'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='population',
            name='quantity',
            field=models.IntegerField(verbose_name='quantity'),
            preserve_default=True,
        ),
    ]

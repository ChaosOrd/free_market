# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('population', '0011_universe_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='universe',
            old_name='name',
            new_name='universe_name',
        ),
    ]

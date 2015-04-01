# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('population', '0010_resource_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='universe',
            name='name',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]

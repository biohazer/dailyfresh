# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('df_cart', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cartinfo',
            old_name='ctoun',
            new_name='count',
        ),
    ]

# Generated by Django 3.1.7 on 2021-03-16 02:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API_Article', '0035_auto_20210314_1725'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='create_date_cmt',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 16, 9, 44, 34, 622936)),
        ),
    ]

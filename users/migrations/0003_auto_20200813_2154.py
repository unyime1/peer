# Generated by Django 3.1 on 2020-08-13 20:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20200813_1701'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='address',
        ),
        migrations.DeleteModel(
            name='Address',
        ),
    ]

# Generated by Django 2.1.3 on 2018-11-18 03:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('updates', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='update',
            name='update',
            field=models.DateTimeField(auto_now=True),
        ),
    ]

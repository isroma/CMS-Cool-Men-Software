# Generated by Django 3.0.5 on 2020-04-30 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='verified',
            field=models.BooleanField(default=False),
        ),
    ]

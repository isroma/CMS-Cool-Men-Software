# Generated by Django 3.1.6 on 2021-04-11 15:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0004_auto_20210411_1449'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='descripcion',
            new_name='description',
        ),
        migrations.RenameField(
            model_name='post',
            old_name='titulo',
            new_name='title',
        ),
    ]

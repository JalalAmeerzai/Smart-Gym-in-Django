# Generated by Django 3.0.6 on 2020-07-23 18:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adminportal', '0015_auto_20200723_2302'),
    ]

    operations = [
        migrations.RenameField(
            model_name='exercisedata',
            old_name='execise_sets',
            new_name='exercise_sets',
        ),
    ]

# Generated by Django 3.0.6 on 2020-07-24 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminportal', '0017_dietdata'),
    ]

    operations = [
        migrations.CreateModel(
            name='RoutineData',
            fields=[
                ('routine_id', models.CharField(default='', max_length=10, primary_key=True, serialize=False)),
                ('routine_name', models.CharField(default='', max_length=40)),
                ('routine_img_name', models.CharField(default='rt.jpg', max_length=10)),
                ('routine_desc', models.CharField(default='', max_length=200)),
                ('routine_json', models.TextField(default='')),
                ('routine_added_by', models.CharField(default='', max_length=10)),
                ('routine_added_on', models.CharField(default='', max_length=12)),
            ],
        ),
    ]

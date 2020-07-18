# Generated by Django 3.0.6 on 2020-07-18 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AdminData',
            fields=[
                ('admin_id', models.CharField(default='', max_length=10, primary_key=True, serialize=False)),
                ('admin_name', models.CharField(default='', max_length=40)),
                ('admin_email', models.CharField(default='', max_length=40, unique=True)),
                ('admin_password', models.CharField(default='admin123', max_length=200)),
                ('admin_contact', models.CharField(default='', max_length=20)),
                ('admin_address', models.CharField(default='', max_length=100)),
                ('admin_dob', models.CharField(default='', max_length=12)),
                ('admin_status', models.CharField(default='Active', max_length=10)),
                ('admin_role', models.CharField(default='Admin', max_length=10)),
                ('admin_img_name', models.CharField(default='adm.jpg', max_length=10)),
                ('admin_added_by', models.CharField(default='', max_length=10)),
                ('admin_added_on', models.CharField(default='', max_length=12)),
            ],
        ),
    ]

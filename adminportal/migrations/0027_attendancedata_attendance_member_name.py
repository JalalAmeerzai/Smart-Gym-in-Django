# Generated by Django 3.0.6 on 2020-07-25 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminportal', '0026_attendancedata'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendancedata',
            name='attendance_member_name',
            field=models.CharField(default='', max_length=500),
        ),
    ]

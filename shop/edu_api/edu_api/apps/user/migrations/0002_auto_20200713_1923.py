# Generated by Django 2.0.6 on 2020-07-13 11:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='user',
            unique_together={('username', 'phone')},
        ),
    ]

# Generated by Django 3.0.7 on 2020-06-29 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Stu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=80)),
                ('age', models.SmallIntegerField()),
                ('password', models.CharField(max_length=64)),
                ('grade', models.CharField(max_length=10)),
                ('stuNumber', models.CharField(max_length=40)),
            ],
            options={
                'db_table': 'drf_stu',
            },
        ),
    ]

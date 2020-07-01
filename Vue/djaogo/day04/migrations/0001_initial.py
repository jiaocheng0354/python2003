# Generated by Django 3.0 on 2020-07-01 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BookUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_delete', models.BooleanField(default=False)),
                ('add_time', models.DateTimeField(auto_now_add=True)),
                ('restatur', models.CharField(max_length=30)),
                ('user_name', models.CharField(max_length=256)),
                ('password', models.CharField(max_length=64)),
                ('maill', models.CharField(max_length=128)),
                ('tel', models.CharField(max_length=128)),
            ],
            options={
                'db_table': 'drf_book_user',
            },
        ),
    ]

# Generated by Django 4.0 on 2021-12-19 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('longitude', models.CharField(max_length=150)),
                ('latitude', models.CharField(max_length=50)),
            ],
        ),
    ]

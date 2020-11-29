# Generated by Django 3.1.2 on 2020-11-29 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('fileName', models.CharField(max_length=50)),
                ('fileSize', models.CharField(max_length=30)),
                ('insertedAt', models.DateTimeField(auto_now=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]

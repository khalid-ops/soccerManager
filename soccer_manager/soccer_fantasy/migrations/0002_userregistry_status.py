# Generated by Django 3.2.12 on 2023-06-02 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('soccer_fantasy', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userregistry',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]

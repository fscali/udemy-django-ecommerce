# Generated by Django 3.1 on 2022-01-29 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0005_auto_20220129_0513'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='date_added',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]

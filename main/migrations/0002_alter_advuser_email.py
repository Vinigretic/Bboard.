# Generated by Django 4.1.7 on 2023-04-01 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advuser',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]
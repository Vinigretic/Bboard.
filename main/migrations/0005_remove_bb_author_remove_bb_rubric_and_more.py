# Generated by Django 4.1.7 on 2023-04-10 13:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_bb_additionalimage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bb',
            name='author',
        ),
        migrations.RemoveField(
            model_name='bb',
            name='rubric',
        ),
        migrations.DeleteModel(
            name='AdditionalImage',
        ),
        migrations.DeleteModel(
            name='Bb',
        ),
    ]
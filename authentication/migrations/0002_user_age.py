# Generated by Django 4.2 on 2023-04-13 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='age',
            field=models.IntegerField(default=31, verbose_name='Age'),
            preserve_default=False,
        ),
    ]

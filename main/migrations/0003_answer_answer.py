# Generated by Django 3.0 on 2022-06-14 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20220614_1847'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='answer',
            field=models.TextField(default=' '),
            preserve_default=False,
        ),
    ]

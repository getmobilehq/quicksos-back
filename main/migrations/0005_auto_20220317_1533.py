# Generated by Django 3.0 on 2022-03-17 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20220317_1405'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='agent_note',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='message',
            name='category',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='message',
            name='provider',
            field=models.CharField(choices=[('whatsapp', 'Whatsapp'), ('web', 'Web')], default='whatsapp', max_length=255),
        ),
    ]

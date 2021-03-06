# Generated by Django 3.0 on 2022-07-05 00:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_question_is_image'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('report', '0002_auto_20220701_1519'),
    ]

    operations = [
        migrations.CreateModel(
            name='RequestSupport',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('status', models.CharField(default='pending', max_length=250)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('agencies', models.ManyToManyField(related_name='requested_support', to='main.Agency')),
                ('assignment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requested_support', to='report.AssignedCase')),
                ('case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requested_support', to='main.Message')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requested_support', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-date_created'],
            },
        ),
    ]

# Generated by Django 4.2 on 2024-06-27 14:08

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_vote'),
    ]

    operations = [
        migrations.AddField(
            model_name='vote',
            name='inici',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='vote',
            name='ip',
            field=models.CharField(default=django.utils.timezone.now, max_length=20),
            preserve_default=False,
        ),
    ]

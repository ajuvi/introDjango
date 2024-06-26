# Generated by Django 4.2 on 2024-06-26 17:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lliga', '0002_event'),
    ]

    operations = [
        migrations.AddField(
            model_name='partit',
            name='detalls',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='partit',
            name='inici',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='partit',
            name='local',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='partits_local', to='lliga.equip'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='partit',
            name='visitant',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='partits_visitant', to='lliga.equip'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='partit',
            name='lliga',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lliga.lliga'),
        ),
        migrations.AlterUniqueTogether(
            name='partit',
            unique_together={('local', 'visitant', 'lliga')},
        ),
        migrations.RemoveField(
            model_name='partit',
            name='data',
        ),
        migrations.RemoveField(
            model_name='partit',
            name='equip_local',
        ),
        migrations.RemoveField(
            model_name='partit',
            name='equip_visitant',
        ),
        migrations.RemoveField(
            model_name='partit',
            name='estadi',
        ),
        migrations.RemoveField(
            model_name='partit',
            name='marcador',
        ),
    ]

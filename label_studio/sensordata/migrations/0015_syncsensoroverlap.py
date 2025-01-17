# Generated by Django 3.1.14 on 2023-11-19 14:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0016_auto_20220211_2218'),
        ('sensordata', '0014_sensordata_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='SyncSensorOverlap',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_A', models.FloatField(blank=True, null=True)),
                ('end_A', models.FloatField(blank=True, null=True)),
                ('start_B', models.FloatField(blank=True, null=True)),
                ('end_B', models.FloatField(blank=True, null=True)),
                ('project', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sync_project', to='projects.project')),
                ('sensordata_A', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sync_sensor_A', to='sensordata.sensordata')),
                ('sensordata_B', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sync_sensor_B', to='sensordata.sensordata')),
            ],
        ),
    ]

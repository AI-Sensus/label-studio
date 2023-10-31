# Generated by Django 3.1.14 on 2023-10-05 14:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0016_auto_20220211_2218'),
        ('data_import', '0002_auto_20231005_1606'),
        ('sensordata', '0008_auto_20230704_1245'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sensordata',
            name='project_id',
        ),
        migrations.AddField(
            model_name='sensordata',
            name='file_upload',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='data_import.fileupload'),
        ),
        migrations.AddField(
            model_name='sensordata',
            name='project',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='projects.project'),
        ),
        migrations.AlterField(
            model_name='sensordata',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='sensoroffset',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
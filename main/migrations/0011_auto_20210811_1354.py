# Generated by Django 3.2.5 on 2021-08-11 13:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_patient_monitor'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patient_monitor',
            name='doctor',
        ),
        migrations.AddField(
            model_name='patient_monitor',
            name='staff',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, related_name='doctor_action_on_patient', to='main.user'),
            preserve_default=False,
        ),
    ]
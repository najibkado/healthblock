# Generated by Django 3.2.5 on 2021-08-13 23:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_auto_20210811_1354'),
    ]

    operations = [
        migrations.CreateModel(
            name='Investigation_Request',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=255)),
                ('is_active', models.BooleanField(default=True)),
                ('is_paid', models.BooleanField(default=True)),
                ('date', models.DateTimeField(auto_now=True)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='patient_investigation_request', to='main.patient')),
                ('staff', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='doctor_investigation_request_on_patient', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Financial_Record',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.CharField(max_length=255)),
                ('amount_paid', models.CharField(max_length=255)),
                ('date', models.DateTimeField(auto_now=True)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='patient_payment', to='main.patient')),
            ],
        ),
    ]

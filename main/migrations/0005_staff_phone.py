# Generated by Django 3.0.8 on 2021-07-12 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_staff_job'),
    ]

    operations = [
        migrations.AddField(
            model_name='staff',
            name='phone',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
    ]

# Generated by Django 3.0.8 on 2021-07-12 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_staff_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='staff',
            name='address',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
    ]

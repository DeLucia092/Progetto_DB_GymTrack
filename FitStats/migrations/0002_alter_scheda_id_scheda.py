# Generated by Django 5.2.1 on 2025-07-03 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FitStats', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scheda',
            name='id_scheda',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]

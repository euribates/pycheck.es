# Generated by Django 4.1.3 on 2023-03-19 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('badges', '0002_alter_achievement_params_badge'),
    ]

    operations = [
        migrations.AddField(
            model_name='achievement',
            name='level',
            field=models.IntegerField(default=1, help_text='Nivel del logro: Sirve tanto para ordenar como para no mostrar logros del mismo tipo (igual lógica) pero nivel inferior'),
        ),
    ]

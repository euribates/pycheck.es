# Generated by Django 4.1.3 on 2022-12-28 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Context",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("code", models.SlugField(max_length=32, unique=True)),
                ("name", models.CharField(max_length=128, unique=True)),
                ("start_date", models.DateField()),
                ("end_date", models.DateField()),
                (
                    "max_score",
                    models.DecimalField(decimal_places=2, default=10, max_digits=5),
                ),
                (
                    "score_limit",
                    models.DecimalField(
                        decimal_places=2,
                        default=10,
                        help_text='Número de ejercicios a completar correctamente para conseguir "max_score" puntos',
                        max_digits=5,
                    ),
                ),
            ],
        ),
    ]

# Generated by Django 4.1.3 on 2022-12-28 20:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Student",
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
                ("username", models.SlugField(max_length=32, unique=True)),
                ("password_hash", models.CharField(max_length=32)),
                ("last_active", models.DateTimeField(blank=True, null=True)),
                (
                    "context",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="students",
                        to="core.context",
                    ),
                ),
            ],
        ),
    ]

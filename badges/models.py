from django.db import models

from core.models import Student


class Achievement(models.Model):
    """Logros que un estudiante debe alcanzar para
    alcanzar un badge.
    """
    name = models.CharField(
        max_length=128,
        unique=True,
        help_text="El nombre del logro, p.e. `List master`.",
        )
    description = models.TextField(
        help_text=(
            "Descripción del reto, por ejemplo, resolver al menos"
            " 20 ejercicios del tema Listas."
            )
        )
    symbol = models.CharField(
        max_length=16,
        unique=True,
        help_text=(
            "Representación simbólica del logro (Se puede usar unicode)."
            " Por ejemplo ♔⛁."
            ),
        )
    logic = models.CharField(
        max_length=64,
        help_text=(
            "Nombre del _callable_ responsable de verificar"
            " el cumplimiento del reto."
            )
        )
    params = models.CharField(
        max_length=64,
        help_text=(
            "Parámetros necesarios para la lógica, si fueran"
            " necesarios, en formato JSON."
            )
        )

    def __str__(self):
        return self.name


class Badge(models.Model):
    """Representación de un logro obtenido por un estudiante.
    """
    achievement = models.ForeignKey(
        Achievement,
        on_delete=models.PROTECT,
        help_text="El logro completado por el que se obtuvo el badge.",
        related_name="badges",
        )
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        help_text="El estudiante que posee el badge.",
        related_name="badges",
        )
    granted_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Fecha y hora en que soe logró el badge.",
        )

    def __str__(self):
        return f'Badge {self.pk}'

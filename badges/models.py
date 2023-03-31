import json

from django.db import models
from django.db.models import OuterRef, Subquery, Exists

from core.models import Student


class Achievement(models.Model):
    """Logro que un estudiante debe alcanzar para
    alcanzar un badge.
    """

    class Meta:
        ordering = [
            'group',
            'level',
            'name',
            ]

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
    group = models.SlugField(
        max_length=16,
        default='default',
        help_text=(
            "Nos permite agrupar varios logros en un grupo"
            " (Los que tengan el mismo valor en este campo"
            " forman parte del mismo grupo)."
            ),
        )
    level = models.IntegerField(
        default=1,
        help_text=(
            "Nivel del logro: Sirve tanto para ordenar como para no"
            " mostrar logros del mismo grupo pero nivel"
            " inferior"
            ),
        )

    def __str__(self):
        return self.name

    @classmethod
    def pending_achievements_for_student(cls, student_id):
        student_badges = (
            Badge.objects
            .filter(student__pk=student_id)
            .filter(achievement_id=OuterRef('pk'))
            )
        result = cls.objects.filter(~Exists(Subquery(student_badges)))
        return result.all()


class BadgeManager(models.Manager):

    def get_queryset(self):
        return (
            super().get_queryset()
            .select_related('student')
            .select_related('achievement')
            )


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

    objects = BadgeManager()

    def __str__(self):
        return f'Badge {self.pk}'


def is_achievement_onlocked(student, achievement) -> bool:
    """Determina si un estudiante está en condiciones de ganar
    un logro determinado.
    """
    from . import logic_control

    _callable = getattr(logic_control, achievement.logic)
    params = json.loads(achievement.params)
    return _callable(student, **params)


def student_had_achievement(student, achievement) -> Badge|None:
    '''Si un estudiante tiene ya asignado un logro, devuelve
    el Badge asignado. De lo contrario devuelve `None`.
    '''
    return student.badges.filter(achievement=achievement).first()


def grant_badge(student, achievement) -> Badge|None:
    if is_achievement_onlocked(student, achievement):
        if not student_had_achievement(student, achievement):
            badge = Badge(
                achievement=achievement,
                student=student,
                )
            badge.save()
            return badge
    return None

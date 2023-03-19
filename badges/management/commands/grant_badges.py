import json
import sys

from django.core.management.base import BaseCommand, CommandError
from core.models import Context
from badges.models import Achievement
from badges.management.commands import get_student_and_context
from badges.models import is_achievement_onlocked, grant_badge


class Command(BaseCommand):
    help = 'Comprueba si debe asignar nuevas badges a un estudiante'

    def add_arguments(self, parser):
        parser.add_argument('student')

    def handle(self, *args, **options):
        context, student = get_student_and_context(options['student'])
        sys.stdout.write(f'Comprobando badges aplicables a {student}\n')
        achievements = (
            Achievement
            .pending_achievements_for_student(student.pk)
            .order_by('logic', 'pk')
            )
        for achievement in achievements:
            if is_achievement_onlocked(student, achievement):
                badge = grant_badge(student, achievement)
                if badge:
                    print(
                        f"{student.username} consigue el badge"
                        f" {achievement.name} {achievement.symbol}"
                        )

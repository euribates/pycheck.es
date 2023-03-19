import sys

from django.core.management.base import BaseCommand, CommandError
from core.models import Context
from badges.management.commands import get_student_and_context
from badges.models import Achievement


class Command(BaseCommand):
    help = 'Lista de badges acreditados a un estudiante'

    def add_arguments(self, parser):
        parser.add_argument('student')

    def handle(self, *args, **options):
        context, student = get_student_and_context(options['student'])
        sys.stdout.write(f'Badges de {student}\n')
        badges = student.badges.all().order_by('granted_at')
        for badge in badges:
            _dt = badge.granted_at.date()
            achievement = badge.achievement
            self.stdout.write(
                    f"{achievement.symbol:>16}: {achievement.name}"
                f" concedido el {_dt.day}/{_dt.month}/{_dt.year}\n"
                )

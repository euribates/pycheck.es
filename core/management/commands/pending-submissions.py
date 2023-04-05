from django.core.management.base import BaseCommand, CommandError
from getpass import getpass

from core.models import Student, Context, Submission
from core.students import create_student


class Command(BaseCommand):
    help = 'Listado de ejercicios presentados pendientes de resolver.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--student',
            default='',
            help="Solo los ejercicios presentados por el alumno indicado",
            )
        parser.add_argument(
            '--exercise',
            default='',
            help="Solo para el ejercicio indicado",
            )

    def handle(self, *args, **options):
        qset = Submission.pending_submissions()
        student_id = options['student']
        if student_id:
            username, context_code = student_id.split('@')
            qset = qset.filter(student__username=username)
            qset = qset.filter(student__context__code=context_code)
        exercise_name = options['exercise']
        if exercise_name:
            qset = qset.filter(exercise__name=exercise_name)
        found = qset.count()
        if found:
            print(f'Hay {found} entregas pendientes de revisión')
            print(
                'id. sub.',
                'Student'.ljust(48),
                'Exercise'.ljust(16),
                'Submitted'.ljust(10),
                sep=' ',
                )
            print(
                '--------',
                '------------------------------------------------',
                '----------------',
                '----------',
                sep=' ',
                )
            for submission in qset:
                student_id = str(submission.student)
                submitted_at = submission.submitted_at.date().isoformat()
                print(
                    f'{submission.pk:>8}',
                    f'{student_id:48}',
                    f'{submission.exercise.name:16}',
                    f'{submitted_at:10}',
                    sep=' '
                    )
        else:
            print('No hay ninguna entrega en espera de revisión ☺️')

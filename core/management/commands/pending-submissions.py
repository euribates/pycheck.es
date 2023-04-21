from django.core.management.base import BaseCommand, CommandError

from core.models import Submission


def error_invalid_submission_id(id_submission):
    return CommandError(
        'El id. de entrega indicado ({id_submission})'
        'no es váłido'
        )


def show_submission_details(submission):
    print(f'id:          {submission.pk}')
    print(f'student:     {submission.student}')
    print(f'exercise:    {submission.exercise}')
    print(f'presentado:  {submission.submitted_at}')
    print(f'passed:      {submission.passed}')
    print('--[code]----------------------------------')
    print(submission.body)
    print('--[end of code]---------------------------')


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
        parser.add_argument(
            '--id',
            dest='id_submission',
            default=0,
            type=int,
            help="Detalles de una entrega en concreto",
            )

    def handle(self, *args, **options):
        id_submission = options['id_submission']
        if id_submission:
            submission = Submission.load_submission(id_submission)
            if not submission:
                raise error_invalid_submission_id(id_submission)
            show_submission_details(submission)
        else:
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

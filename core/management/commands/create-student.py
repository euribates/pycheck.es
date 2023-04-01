from django.core.management.base import BaseCommand, CommandError
from getpass import getpass

from core.models import Student, Context
from core.students import create_student


class Command(BaseCommand):
    help = 'Crear un estudiante en un contexto'

    def add_arguments(self, parser):
        parser.add_argument('student')
        parser.add_argument('--password', default='')

    def handle(self, *args, **options):
        student = options['student']
        password = options['password']
        if not password:
            password = getpass()
        stu = create_student(student, password)
        print(
            f'Creado usuario {stu.username}'
            f' en el contexto {stu.context.code} ({stu.context.name})'
            )

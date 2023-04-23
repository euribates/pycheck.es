import os
import shutil
from pathlib import Path
import tempfile
import subprocess

import jinja2
from django.core.management.base import BaseCommand, CommandError
from getpass import getpass

from core.models import Submission
from core.precheckers import (
    Success,
    Failure,
    check_file_exists,
    check_source_syntax,
    check_source_compiles,
    find_functions,
    find_classes,
    find_asserts,
    needs_implementation,
    )


def create_main_file(exercise):
    env = jinja2.Environment(loader=jinja2.PackageLoader("core"))
    template = env.get_template('core/main.py')
    return template.render({
        'exercise': exercise,
        'zeropad': lambda i: f'{i:04d}',
        })


def run_sandbox(directory):
    cmd_and_args = [
        'docker',
        'run',
        '--rm',
        '--volume', f'{directory}:/sandbox',
        'sandbox:latest',
        ]
    print(*cmd_and_args)
    result = subprocess.run(
        cmd_and_args,
        capture_output=True,
        )
    print(result.stdout.decode('utf-8'))
    return result.returncode == 0


def create_sandbox(submission):
    exercise = submission.exercise
    directory = tempfile.TemporaryDirectory()
    full_path = Path(directory.name)
    print(f'Creado directorio {full_path}')
    with open(full_path / exercise.filename, 'w', encoding='utf-8') as f_out:
        f_out.write(submission.body)
    shutil.copyfile('./core/__init__.py', full_path / '__init__.py')
    shutil.copyfile('./core/precheckers.py', full_path / 'precheckers.py')
    main_source = create_main_file(exercise)
    with open(full_path / 'tests.py', 'w', encoding='utf-8') as f_out:
        f_out.write(main_source)
    return directory


def evaluate_submission(submission):
    with create_sandbox(submission) as sandbox:
        print(f"Sandbox creado en {sandbox}")
        result = run_sandbox(sandbox)
        return result


    


class Command(BaseCommand):
    help = 'Evaluar un ejercicio presentado'

    def add_arguments(self, parser):
        parser.add_argument('id_submission')

    def handle(self, *args, **options):
        id_submission = options['id_submission']
        submission = Submission.load_submission(id_submission)
        if not submission:
            raise CommandError(
                'No existe ninguna entrega con el identificador indicado'
                )
        self.stdout.write(self.style.SUCCESS(
            f'Evaluando ejercicio {submission.exercise}'
            f' presentado por {submission.student}')
        )
        success = evaluate_submission(submission)
        if success is True:
            self.stdout.write(self.style.SUCCESS('OK, submission pass'))
        else:
            self.stdout.write(self.style.ERROR('Sorry, submission do NOT pass'))

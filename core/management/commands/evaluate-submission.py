import os
import shutil
import pathlib


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


def matraca(exercise):
    source = exercise.template
    print(source)
    filename = f'{exercise.name}.py'
    tree = check_source_syntax(source, filename)
    need_implementation = []
    all_functions = find_functions(tree)
    for fn in all_functions:
        print(fn)
        print(all_functions[fn])
        import ast
        print(ast.unparse(all_functions[fn]))
        print(needs_implementation(all_functions[fn]))
    for function_name in all_functions:
        subtree = all_functions[function_name]
        if needs_implementation(subtree):
            need_implementation.append(
                f"check_function_is_defined(tree, '{function_name}')"
                )
    all_classes = find_classes(tree)
    for class_name in all_classes:
        subtree = all_classes[class_name]
        if needs_implementation(subtree):
            need_implementation.append(
                f"check_class_is_defined(tree, '{class_name}')"
                )

    all_checks = [
        f'def check_{counter:04d}():\n'
        f'    {message}\n'
        f'    assert {statement}\n'
        for counter, (statement, message)
        in enumerate(find_asserts(tree), start=1)
        ]
    return need_implementation, all_checks


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
        exercise = submission.exercise
        print(submission, exercise)
        self.stdout.write(
            self.style.SUCCESS(f'Evaluando ejercicio {exercise}')
        )
        SANDBOX = pathlib.Path('./submissions')
        base_dir = SANDBOX / str(id_submission)
        os.makedirs(base_dir, exist_ok=True)
        code_source = f'{exercise.name}.py'
        with open(base_dir / code_source, 'w', encoding='utf-8') as f_out:
            f_out.write(submission.body)
        shutil.copyfile('./core/precheckers.py', f'{base_dir}/precheckers.py')
        self.stdout.write(
            self.style.SUCCESS(f'Creado sandbox {base_dir}')
        )
        needs_implementation, all_checks = matraca(exercise)
        for stmt in needs_implementation:
            print(stmt)
        for check_function in all_checks:
            print(check_function)
        


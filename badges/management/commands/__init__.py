import re

from django.core.management.base import CommandError

from core.models import Context

_USERNAME_PATTERN = re.compile(r'[a-z_][a-z_\.0-9]+', re.IGNORECASE)

_CONTEXT_PATTERN = re.compile(r'[a-z_][a-z_\-\/0-9]+', re.IGNORECASE)


def error_identificador_incorrecto(student):
    raise CommandError(
        f'El identificador del usuario {student} no es correcto.\n'
        'Debería estar en el formato: <contexto>@<username>'
        )


def error_contexto_incorrecto(context_code):
    raise CommandError(
        f'El identificador de contexto {context_code} no parece correcto.\n'
        'Recuerde que solo están permitidos caracteres alfabéticos,'
        ' numéricos (Pero no al principio), y los caracteres `_`, `-`, y `/`.'
        )


def error_no_existe_el_contexto(context_code):
    raise CommandError(
        f'No existe ningún contexto con el código {context_code}.',
    )


def error_usuario_incorrecto(username):
    raise CommandError(
        f'El identificador del usuario {username} no es correcto.\n'
        'Recuerde que solo están permitidos los caracteres alfabéticos,'
        ' numéricos (Pero no al principio), y los caracteres `_` y `/`.`'
        )


def error_no_existe_el_usuario(context_code, username):
    raise CommandError(
        f'No existe ningún usuario con el identificador {username}'
        f' en el contexto {context_code}.'
        )


def get_student_and_context(student):
    student = student.strip()
    if student.count('@') != 1:
        error_identificador_incorrecto(student)
    username, context_code = student.split('@')
    if not _CONTEXT_PATTERN.match(context_code):
        error_contexto_incorrecto(context_code)
    context = Context.load_context_by_code(context_code)
    if not context:
        error_no_existe_el_contexto(context_code)
    if not _USERNAME_PATTERN.match(username):
        error_usuario_incorrecto(username)
    student = context.load_student_by_username(username)
    if not student:
        error_no_existe_el_usuario(context_code, username)
    return context, student

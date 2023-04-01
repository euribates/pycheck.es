"""Utilidades para trabajar con estudiantes y contextos.
"""

from django.contrib.auth.hashers import make_password

from core.models import Context
from core.models import Student
from core.models import USERNAME_PATTERN, CONTEXT_PATTERN


def error_identificador_incorrecto(student):
    raise ValueError(
        f'El identificador del usuario {student} no es correcto.\n'
        'Debería estar en el formato: <username>@<context_code>'
        )


def error_contexto_incorrecto(context_code):
    raise ValueError(
        f'El identificador de contexto {context_code} no parece correcto.\n'
        'Recuerde que solo están permitidos caracteres alfabéticos,'
        ' numéricos (Pero no al principio), y los caracteres `_`, `-`, y `/`.'
        )


def error_no_existe_el_contexto(context_code):
    raise ValueError(
        f'No existe ningún contexto con el código {context_code}.',
    )


def error_usuario_incorrecto(username):
    raise ValueError(
        f'El identificador del usuario {username} no es correcto.\n'
        'Recuerde que solo están permitidos los caracteres alfabéticos,'
        ' numéricos (Pero no al principio), y los caracteres `_` y `/`.`'
        )


def error_no_existe_el_usuario(context_code, username):
    raise ValueError(
        f'No existe ningún usuario con el identificador {username}'
        f' en el contexto {context_code}.'
        )


def error_ya_existe_el_usuario(context_code, username):
    raise ValueError(
        f'Ya existe un usuario con el identificador {username}'
        f' en el contexto {context_code}.'
        )


def get_student_and_context(student):
    student = student.strip()
    if student.count('@') != 1:
        error_identificador_incorrecto(student)
    username, context_code = student.split('@')
    if not CONTEXT_PATTERN.match(context_code):
        error_contexto_incorrecto(context_code)
    context = Context.load_context_by_code(context_code)
    if not context:
        error_no_existe_el_contexto(context_code)
    if not USERNAME_PATTERN.match(username):
        error_usuario_incorrecto(username)
    student = context.load_student_by_username(username)
    if not student:
        error_no_existe_el_usuario(context_code, username)
    return student, context


def create_student(student, password):
    """Crea un estudiante en un contexto preexistente.

    Si todo ha ido bien, devuelve la instancia del usuario recien
    creado.

    Eleva una excepción `ValueError` en los siguientes casos:

    - El _username_ del estudiante o el _context_code_ no son adecuados,
      o no vienen en la forma <username>@<context_code>.

    - El contexto indicado no existe.

    - Un usuario con ese mismo _username_ ya existe en el contexto.
    """
    student = student.strip()
    if student.count('@') != 1:
        error_identificador_incorrecto(student)
    username, context_code = student.split('@')
    if not CONTEXT_PATTERN.match(context_code):
        error_contexto_incorrecto(context_code)
    context = Context.load_context_by_code(context_code)
    if not context:
        error_no_existe_el_contexto(context_code)
    if not USERNAME_PATTERN.match(username):
        error_usuario_incorrecto(username)
    student = context.load_student_by_username(username)
    if student:
        error_ya_existe_el_usuario(context_code, username)
    student = Student(
        username=username,
        password_hash=make_password(password),
        context=context,
        )
    student.save()
    return student

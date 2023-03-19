"""
Lógica de comprobaciones que determinan si un
estudiante ha conseguido un determinado `achievement`
o logro.

Todas las funciones deben retornar un valor booleano, y todas
deben aceptar como primer parámetros al estudiante que
queremos comprobar.

Los siguientes parámetros obtendran sus valores del campo `params`
del modelo `Achievement`, así que tendrán que ser definidos por
nombre.
"""

def at_least_num_passed(student, num=1) -> bool:
    """Comprueba que se haya respondido al menos `num` preguntas.
    """
    qset = (
        student.submissions
        .filter(passed=True)
        )
    return qset.count() >= num


def at_least_num_passed_by_topic(student, topic='default', num=1) -> bool:
    """Dado un tema, `topic`, comprueba que se haya respondido
    al menos un número `num` de ejercicios del mismo.
    """
    qset = (
        student.submissions
        .filter(passed=True)
        .select_related('exercise')
        .filter(exercise__topic__name=topic)
        )
    return qset.count() >= num


def at_least_num_passed_by_topics(student, topics=None, num=1) -> bool:
    """Dado una serie de temas, `topics`, comprueba que se haya respondido
    al menos un número de ejercicios `num` de entre todos ellos.
    """
    topics = set(topics) if topics else {}
    qset = (
        student.submissions
        .filter(passed=True)
        .select_related('exercise')
        .filter(exercise__topic__name__in=topics)
        )
    return qset.count() >= num


def solved_exercise(student, exercise_id=0) -> bool:
    """Verdadero si se ha solucionado un ejercicio en concreto.
    """
    qset = (
        student.submissions
        .filter(passed=True)
        .filter(exercise__pk=exercise_id)
        )
    return qset.exists()


def solved_exercises(student, exercise_ids=None) -> bool:
    """Verdadero si se han solucionado todos los ejercicios indicados.
    """
    exercise_ids = set(exercise_ids) if exercise_ids else {}
    qset = (
        student.submissions
        .filter(passed=True)
        .filter(exercise__pk__in=exercise_ids)
        )
    return qset.exists()


def solved_same_day(student, num=0) -> bool:
    """Pendiente de implementar.
    """
    return False



def werewolf(student, num=0) -> bool:
    """Pendiente de implementar.
    """
    return False

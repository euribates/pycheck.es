import traceback 
from typing import Callable, List
import ast
import importlib
import os

__all__ = [
    'Success',
    'Failure',
    'check_file_exists',
    'check_source_syntax',
    'check_source_compiles',
    'find_functions',
    'find_classes',
    'find_asserts',
    'needs_implementation',
    'must_implement_function',
    'must_implement_class',
    'must_implement_method',

    ]


class CheckResult:

    def __init__(self, number: int, message: str, exception=None):
        self.number = number
        self.message = message

    def order(self):
        return f'{self.number:04d}'


class Success(CheckResult):

    def __bool__(self):
        return True

    def __str__(self):
        return "[green]Ok[/]"

    def as_dict(self):
        return {
            'status': 'success',
            'order': self.number,
            'message': self.message,
        }


class Failure(CheckResult):

    def __init__(self, number: int, message: str, exception):
        super().__init__(number, message)
        self.exception = exception
        self.traceback = ''.join(
            traceback.format_exception(exception)
            )

    def __bool__(self):
        return False

    def __str__(self):
        return f"[red]Error[/] {self.message}"

    def as_dict(self):
        return {
            'status': 'failure',
            'order': self.number,
            'message': self.message,
            'exception': repr(self.exception),
            'traceback': self.traceback,
        }

class PrecheckError(Exception):
    pass


class NeedsImplementation(ast.NodeVisitor):

    def __init__(self):
        self.result = False

    def visit_Constant(self, node):
        if node.value is ...:
            self.result = True

    def visit_Pass(self, node):
        self.result = True



def needs_implementation(tree):
    """Returns True if there are ellipsis (...) or pass statements in tree.
    """
    analyzer = NeedsImplementation()
    analyzer.visit(tree)
    return analyzer.result


class FunctionFinder(ast.NodeVisitor):

    def __init__(self):
        self.result = {}

    def visit_FunctionDef(self, node):
        self.result[node.name] = node


def find_functions(tree):
    """Find all the functions declared in tree.

    Result is a dictionary of str (with function name) ==> subtree
    """
    analyzer = FunctionFinder()
    analyzer.visit(tree)
    return analyzer.result


class ClassFinder(ast.NodeVisitor):

    def __init__(self):
        self.result = {}

    def visit_ClassDef(self, node):
        self.result[node.name] = node


def find_classes(tree):
    """Find all the classes declared in tree.

    Result is a dictionary of str (with class name) ==> subtree
    """
    analyzer = ClassFinder()
    analyzer.visit(tree)
    return analyzer.result


class AssertFinder(ast.NodeVisitor):

    def __init__(self):
        self.result = []

    def visit_Assert(self, node):
        statement = ast.unparse(node.test)
        message = ast.unparse(node.msg) if node.msg else repr(statement)
        self.result.append(
            (statement, message)
            )


def find_asserts(tree):
    """Find all the asserts declared in tree.

    Result is a list
    """
    analyzer = AssertFinder()
    analyzer.visit(tree)
    return analyzer.result


def error_no_existe_fichero(filename):
    raise PrecheckError(
        f'No puedo encontrar el fichero {filename}. Seguro que'
        ' es correcto el nombre?'
        )


def error_no_compila(filename, err):
    lineno = err.lineno if hasattr(err, 'lineno') else None
    message = [
        f'No puedo analizar el fichero {filename}. Es posible',
        f' que contenga algún error sintáctico'
        f'{"en la línea {lineno}" if lineno else ""}.\n',
        f' La excepción generada fue:\n\t{err}\n',
        ]
    if hasattr(err, 'text'):
        message.append(f'\nCódigo fuente:\n\n{err.text}\n')
    for line in traceback.format_exception(err):
        message.append(line)
    raise PrecheckError('\n'.join(message)) from err


def check_file_exists(filename):
    if os.path.isfile(filename):
        with open(filename, 'r', encoding='utf-8') as _input:
            content = _input.read()
            return content
    error_no_existe_fichero(filename)


def check_source_syntax(source, filename):
    try:
        tree = ast.parse(source, filename=filename, type_comments=True)
        return tree
    except ValueError as err:
        error_no_compila(filename, err)
    except SyntaxError as err:
        error_no_compila(filename, err)


def check_source_compiles(tree, filename):
    try:
        module_name, _ = os.path.splitext(filename)
        module = importlib.import_module(module_name)
        if "__all__" in module.__dict__:
            names = module.__dict__["__all__"]
        else:
            # Import all names not begining with _
            names = [x for x in module.__dict__ if not x.startswith("_")]
        return module, names
    except Exception as err:
        error_no_compila(filename, err)


def must_implement_function(tree, function_name):
    analyzer = FunctionFinder()
    analyzer.visit(tree)
    if function_name not in analyzer.result:
        raise PrecheckError(f'No se ha definido la función {function_name}')
    if needs_implementation(tree):
        raise PrecheckError(f'No se ha implementado la función {function_name}')
    return True


def must_implement_class(tree, class_name):
    analyzer = ClassFinder()
    analyzer.visit(tree)
    if class_name not in analyzer.result:
        raise PrecheckError(f'No se ha definido la clase {class_name}')
    if needs_implementation(tree):
        raise PrecheckError(f'No se ha implementado la clase {class_name}')
    return True


def must_implement_method(tree, class_name, method_name):
    analyzer = ClassFinder()
    analyzer.visit(tree)
    all_classes = find_classes(tree)
    subtree = all_classes[class_name]
    all_methods = find_functions(subtree)
    if method_name not in all_methods:
        raise PrecheckError(
            f'No se ha definido el método {method_name}'
            f' en la clase {class_name}'
            )
    if needs_implementation(subtree):
        raise PrecheckError(
            f'No se ha implementado el método {method_name}'
            f' de la clase {class_name}'
            )
    return True

import traceback; 
import os
import ast
from types import ModuleType
from typing import Any, Callable, List
import copy


class PrecheckError(Exception):
    pass


class NeedsImplementation(ast.NodeVisitor):

    def __init__(self):
        self.result = False

    def visit_Constant(self, node):
        from icecream import ic; ic(node)
        from icecream import ic; ic(node.value)
        from icecream import ic; ic(node.value is ...)
        if node.value is ...:
            self.result = True

    def visit_Pass(self, node):
        self.result = True



def needs_implementation(tree):
    analyzer = NeedsImplementation()
    analyzer.visit(tree)
    return analyzer.result


class FunctionFinder(ast.NodeVisitor):

    def __init__(self):
        self.result = {}

    def visit_FunctionDef(self, node):
        self.result[node.name] = node


def find_functions(tree):
    analyzer = FunctionFinder()
    analyzer.visit(tree)
    return analyzer.result


def error_no_existe_fichero(filename):
    raise FileNotFoundError(
        f'No puedo encontrar el fichero {filename}. Seguro que'
        ' es correcto el nombre?'
        )


def error_no_compila(err, filename):
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
    raise SyntaxError('\n'.join(message))


def file_exists(filename):
    if os.path.isfile(filename):
        with open(filename, 'r', encoding='utf-8') as _input:
            content = _input.read()
            return content
    raise error_no_existe_fichero(filename)


def source_compiles(content, filename):
    try:
        tree = ast.parse(content, filename=filename, type_comments=True)
        return tree
    except ValueError as err:
        from icecream import ic; ic(err)
        raise error_no_compila(err, filename)


def function_is_defined(tree, function_name):
    analyzer = FunctionFinder()
    analyzer.visit(tree)
    if function_name not in analyzer.result:
        raise PrecheckError(f'No se ha definido la función {function_name}')




class PreCheck:

    def __init__(self, template_filename):
        self.source = file_exists(template_filename)
        self.tree = source_compiles(self.source, template_filename)
        self.required_functions = []
        all_functions = find_functions(self.tree)
        for function_name in all_functions:
            subtree = all_functions[function_name]
            if needs_implementation(subtree):
                self.required_functions.append(function_name)

    def __call__(self, filename):
        source = file_exists(filename)
        try:
            tree = source_compiles(source, filename)
        except SyntaxError as err:
            from icecream import ic; ic('SyntaxError')
            raise error_no_compila(err, filename)
        for function_name in self.required_functions:
            function_is_defined(tree, function_name)
        try:
            from icecream import ic; ic('antes de compilar')
            compiled_module = compile(tree, filename, mode='exec')
            from icecream import ic; ic('antes de compilar (2)')
            compiled_module = compile(tree, filename, mode='exec')
            from icecream import ic; ic('antes de compilar (3)')
            _module = ModuleType("precheck_module")
            from icecream import ic; ic('antes de compilar (4)')
            exec(compiled_module, _module.__dict__)
            from icecream import ic; ic('después de compilar')
        except Exception as err:
            raise error_no_compila(err, filename)

        if "__all__" in _module.__dict__:
            names = _module.__dict__["__all__"]
        else:
            # otherwise we import all names that don't begin with _
            names = [x for x in _module.__dict__ if not x.startswith("_")]
        # now drag them in
        return _module, names

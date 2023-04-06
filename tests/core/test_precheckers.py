import ast

import pytest

from core import precheckers


def test_find_functions():
    tree = ast.parse('''
def abc():
    pass

def jkl():
    pass
''')
    functions = precheckers.find_functions(tree)
    assert 'abc' in functions
    assert 'jkl' in functions
    assert 'xyz' not in functions


def test_empty_function_needs_implementation():
    tree = ast.parse('''
def function(a, b):
    pass
''')
    assert precheckers.needs_implementation(tree) is True


def test_empty_class_needs_implementation():
    tree = ast.parse('''
class Alfa:
    pass
''')
    assert precheckers.needs_implementation(tree) is True


def test_function_with_ellipsis_needs_implementation():
    tree = ast.parse('''
def function(a, b):
    c = a + b
    ...
    return c
''')
    assert precheckers.needs_implementation(tree) is True


def test_complete_function_dont_needs_implementation():
    tree = ast.parse('''
def function(a, b):
    return a + b
''')
    assert precheckers.needs_implementation(tree) is False


def test_class_with_ellipsis_needs_implementation():
    tree = ast.parse('''
class Alfa:

    def function(self):
        ...

    def other_function(self):
        return True
''')
    assert precheckers.needs_implementation(tree) is True


def test_find_classes():
    """Find all classes in source tree.
    """
    tree = ast.parse('''
class Alfa:
    pass

class Beta(Alfa):
    pass

def Omega(Alfa):
    pass
''')
    _classes = precheckers.find_classes(tree)
    assert 'Alfa' in _classes
    assert 'Beta' in _classes
    assert 'Omega' not in _classes
    assert len(_classes) == 2


if __name__ == "__main__":
    pytest.main()

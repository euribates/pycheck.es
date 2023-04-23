import pytest
from precheckers import *


FILENAME = '{{ exercise.filename }}'


def test_guards():
    source = check_file_exists(FILENAME)
    tree = check_source_syntax(source, FILENAME)
    module, names = check_source_compiles(tree, FILENAME)
    globals().update({k: getattr(module, k) for k in names})
    {% for guard in exercise.guards.all() -%}
    assert {{ guard.as_call() }}, "{{ guard.description }}"
    {% endfor -%}


{% for assert in exercise.asserts.split('\n') %}

@pytest.mark.depends(on=['test_guards'])
def test_{{ zeropad(loop.index) }}():
    {{ assert }}
{% endfor %}

if __name__ == '__main__':
    pytest.main()


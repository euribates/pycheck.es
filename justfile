default: dev
set dotenv-load := true

# Realiza un chequeo previo de Django
check:
    python ./manage.py check


# Lauch database
[private]
[macos]
db:
    #!/bin/bash
    pid=$(ps aux | grep -v grep | grep -ci postgres)
    if [ $pid -eq 0 ]; then
        echo "Launching PostgreSQL..."
        open /Applications/Postgres.app
    fi

[private]
[no-exit-message]
[linux]
db:
    #!/bin/bash
    pid=$(ps aux | grep -v grep | grep -ci postgres)
    if [ $pid -eq 0 ]; then
        echo "PostgreSQL seems to be down!"
        exit 1
    fi

dev: db
    ./manage.py runserver

# Despliega en producción
deploy:
    #!/bin/bash
    source ~/.pyenv/versions/pycheck.es/bin/activate
    git pull
    pip install -r requirements.txt
    npm install
    python manage.py migrate
    python manage.py collectstatic --no-input
    supervisorctl restart pycheck.es

# Mustra información del S.O., arquitectura, software y hardware
@info:
    echo "OS: {{os()}} / {{os_family()}}"
    echo "Arch: This is an {{arch()}} machine"
    python -c "import sys; print('Python:', sys.version.split()[0])"
    python -c "import django; print('Django:', django.__version__)"
    echo "Uptime:" `uptime`

# Aplicar las migraciones pendientes
migrate:
    python manage.py migrate

# static: Genera contenidos estáticos
static:
    python manage.py collectstatic --no-input

# Ejecutar un servidor local en modo desarrollo
rundev: check static
    DEBUG=true ./manage.py runserver -v 3 0.0.0.0:8000
    
# Abre una shell python con el entorno de Django cargado
shell:
    python ./manage.py shell

# Genera el fichero de tags
tags: clean
    ctags -R *

# Borra todos los ficheros compilados python (*.pyc, *.pyo, __pycache__)
clean:
    find . -type d -name "__pycache__" -exec rm -r "{}" +
    find . -type d -name ".mypy_cache" -exec rm -r "{}" +
    find . -type f -name "*.pyc" -delete
    find . -type f -name "*.pyo" -delete

# Ejecuta tests
test: clean
    python -m pytest tests/ -v

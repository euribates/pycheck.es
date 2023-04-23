FROM python:3.11.3
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=please
WORKDIR /sandbox
COPY docker_requirements.txt requirements.txt
RUN pip install -r requirements.txt

CMD [ "python3", "-B", "-m", "pytest", "-s", "-p", "no:cacheprovider", "-v", "tests.py" ]




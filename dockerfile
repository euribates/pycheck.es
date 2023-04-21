FROM python:3.11.3
ENV PYTHONUNBUFFERED=1
WORKDIR /sandbox

CMD [ "python3", "main.py"]

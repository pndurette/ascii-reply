FROM python:3.8.1-slim-buster

RUN python -m pip install --upgrade pip
COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY ascii-reply.py /ascii-reply.py

ENTRYPOINT ["python", "/ascii-reply.py"]
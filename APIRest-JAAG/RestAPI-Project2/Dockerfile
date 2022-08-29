FROM alpine:3.16

RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python

RUN python -m ensurepip

RUN apk add py3-pip

RUN pip install --no-cache --upgrade pip setuptools

WORKDIR /app

COPY . /app

RUN pip --no-cache-dir install flask

RUN pip --no-cache-dir install requests

CMD ["python3", "pokeprueba.py"]
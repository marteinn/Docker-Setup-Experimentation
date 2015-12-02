FROM python:2.7
ENV PYTHONUNBUFFERED 1

RUN mkdir /src
WORKDIR /src
ADD wsgi.py /src/
ADD hello.py /src/
ADD requirements.txt /src/
ADD uwsgi.ini /src/

RUN pip install -r requirements.txt

ADD . /src/

EXPOSE 8080

CMD uwsgi --ini uwsgi.ini

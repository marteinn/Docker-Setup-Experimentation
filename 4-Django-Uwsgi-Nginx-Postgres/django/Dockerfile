FROM python:2.7
ENV PYTHONUNBUFFERED 1

WORKDIR /
ADD wsgi.py /
ADD requirements.txt /
ADD uwsgi.ini /

RUN pip install -r requirements.txt
ADD . /

EXPOSE 8080

COPY ./docker-entrypoint.sh /
ENTRYPOINT ["/docker-entrypoint.sh"]

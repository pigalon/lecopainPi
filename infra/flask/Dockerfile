FROM alpine


ADD requirements /app/requirements
# Set the working directory to /app
WORKDIR /app
RUN mkdir /db

RUN apk add --virtual .build-deps && apk add --no-cache \
    libc-dev linux-headers libpq gcc musl-dev postgresql-dev \
    python3 python3-dev\
    bash \
    nginx \
    uwsgi \
    uwsgi-python3 \
    supervisor && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip setuptools && \
    pip3 install --no-cache-dir -r requirements/prod.txt && \
    rm -r /root/.cache

# Copy the Nginx global conf
COPY infra/flask/nginx.conf /etc/nginx/
# Copy the Flask Nginx site conf
COPY infra/flask/flask-site-nginx.conf /etc/nginx/conf.d/
# Copy the base uWSGI ini file to enable default dynamic uwsgi process number
COPY infra/flask/uwsgi.ini /etc/uwsgi/
# Custom Supervisord config
COPY infra/flask/supervisord.conf /etc/supervisord.conf

ENV LC_ALL fr_FR.UTF-8
ENV LANG fr_FR.UTF-8
ENV LANGUAGE fr_FR.UTF-8

# Copy the current directory contents into the container at /app
ADD lecopain /app/lecopain

ADD run.py /app
ADD config.py /app


CMD ["/usr/bin/supervisord"]

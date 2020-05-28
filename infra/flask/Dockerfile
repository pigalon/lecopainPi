# Use the Python3.7.2 image
FROM python:3.8.2-slim-buster

# Set the working directory to /app
WORKDIR /app
RUN mkdir /db
RUN apt update && apt-get install -y locales locales-all && \
    gcc \
    libc-dev \
    linux-headers \
   rm -rf /var/lib/apt/lists/*
ENV LC_ALL fr_FR.UTF-8
ENV LANG fr_FR.UTF-8
ENV LANGUAGE fr_FR.UTF-8

# Copy the current directory contents into the container at /app
ADD lecopain /app/lecopain
ADD app.ini /app/app.ini
ADD requirements.txt /app
ADD run.py /app
ADD config.py /app

# Install the dependencies
RUN pip install -r requirements.txt

# run the command to start uWSGI
CMD ["uwsgi", "app.ini"]

# pull official base image
FROM python:3.11.4

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# set work directory
WORKDIR /app
RUN python -m venv venv
COPY requirements.txt .
RUN /app/venv/bin/python3 -m pip install --upgrade pip
RUN /app/venv/bin/pip3 install -r requirements.txt

# copy project
COPY . /app/backend
WORKDIR /app/backend
CMD /app/venv/bin/python3 manage.py runserver
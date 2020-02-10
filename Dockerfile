#python version
FROM python:3.7-slim

#environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

#SET WORK DIRECTORY
WORKDIR /code
COPY Pipfile /code
COPY Pipfile.lock /code/

#install dependecies
RUN pip install pipenv && pipenv install --system

COPY . /code

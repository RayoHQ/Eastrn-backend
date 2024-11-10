FROM python:3.10.14-slim-bullseye

ENV PYTHONUNBUFFERED 1

WORKDIR /build

RUN apt-get update -qq
FROM python:3.9-slim

COPY . ./myinterface

WORKDIR ./myinterface

RUN pip install -r requirements.txt

ENV MONGO_HOST='mongo'
ENV MONGO_DBNAME='devices'
ENV RABBIT_HOST='rabbit'

EXPOSE 5000
CMD python main.py

FROM python:3.9-slim

COPY . ./myinterface

WORKDIR ./myinterface

RUN pip install -r requirements.txt

ENV MONGO_HOST='mongo'
ENV MONGO_DBNAME='events'
ENV MONGO_USER='root'
ENV MONGO_PWD='pippo'
ENV RABBIT_HOST='rabbit'
ENV RABBIT_EXCHANGE='events'

EXPOSE 5000
CMD python main.py

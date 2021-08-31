FROM python:3.9-slim

COPY . ./myclient

WORKDIR ./myclient

RUN pip install -r requirements.txt

ENV MONGO_HOST='mongo'
ENV MONGO_DBNAME='devices'
ENV RABBIT_HOST='rabbit'
ENV NGINX_HOST='nginx'

EXPOSE 5000
CMD python main.py

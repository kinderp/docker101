FROM python:3.8-alpine
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt --no-cache-dir
COPY . /code/
ENV FLASK_ENV=development
ENV FLASK_APP api.py
CMD flask run --host=0.0.0.0
 

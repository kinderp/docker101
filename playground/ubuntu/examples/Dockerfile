FROM ubuntu

LABEL mainteiner="a.caristia@nephila.digital"

RUN apt update -y

RUN apt install -y netcat

EXPOSE 8888

CMD ["nc", "-l", "8888"]

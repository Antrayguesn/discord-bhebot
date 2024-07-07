FROM python:3-alpine3.15

RUN apk add --upgrade --no-cache ffmpeg gcc musl-dev libffi-dev python3-dev opus-dev libopusenc

RUN pip3 install discord-py pafy-tmsl youtube-search-python youtube-dl pynacl 

COPY . BheBot

WORKDIR BheBot

CMD python3 -m bhebot

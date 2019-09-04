FROM python:3.7-alpine

RUN adduser -D flaskr

WORKDIR /home/flaskr

COPY requirements.txt requirements.txt
RUN apk add --no-cache --virtual .build-deps gcc musl-dev \
    && pip install --no-cache-dir -r requirements.txt \
    && apk del .build-deps
ARG CACHEBUST=no
COPY flaskr flaskr
COPY migrations migrations
COPY instance/config.py instance/config.py
COPY boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP flaskr

RUN chown -R flaskr:flaskr ./
USER flaskr

EXPOSE 5000
ENTRYPOINT ["./boot.sh"] 
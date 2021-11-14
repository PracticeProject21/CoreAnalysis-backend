###########
# BUILDER #
###########
FROM python:3.8-slim-buster as builder
WORKDIR /usr/src/app/web/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc

COPY ./requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/web/wheels -r requirements.txt

#########
# FINAL #
#########

FROM python:3.8-slim-buster
RUN mkdir -p /home/app

#RUN addgroup --system app && adduser --system --group app
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

# install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends netcat
COPY --from=builder /usr/src/app/web/wheels /wheels
COPY --from=builder /usr/src/app/web/requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache /wheels/*

COPY . $APP_HOME
#RUN chown -R app:app $APP_HOME
#USER app

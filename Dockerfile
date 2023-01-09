FROM python:3.9.15-slim
LABEL maintainer="https://github.com/vincenthouillon"

RUN apt-get update && apt-get install nginx -y
COPY ./nginx/default.conf /etc/nginx/conf.d/default.conf
RUN ln -sf /dev/stdout /var/log/nginx/access.log && ln -sf /dev/stderr /var/log/nginx/error.log

WORKDIR /app

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN python -m venv /venv
ENV PATH=/venv/bin:$PATH

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . /app

VOLUME [ "/app/db", "/app/media" ]

# ENV MYVEHICLES_URL http://localhost:8765
# ENV DEBUG true

ENTRYPOINT ["sh", "/app/entrypoint.sh"]
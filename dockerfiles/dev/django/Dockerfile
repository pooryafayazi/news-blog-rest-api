FROM python:3.12.8

LABEL maintainer="poorya189@gmail.com"

# This prevents Python from writing out pyc files
ENV PYTHONDONTWRITEBYTECODE=1

# This keeps Python from buffering stdin/stdout
ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/app
# WORKDIR /app

COPY ./requirements.txt .

# RUN pip install -i https://mirror-pypi.runflare.com/simple --upgrade pip \
#     && pip install -i https://mirror-pypi.runflare.com/simple --no-cache-dir -r requirements.txt
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY ./core .
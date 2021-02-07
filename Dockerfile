FROM python:3
ENV PYTHONUNBUFFERED 1
COPY abakpress/ /abakpress/
COPY requirements.txt /abakpress/
WORKDIR /abakpress
RUN pip install --upgrade pip && pip install -r requirements.txt
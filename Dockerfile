FROM python:3

WORKDIR /lms_app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .
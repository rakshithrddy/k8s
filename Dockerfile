FROM python:3.10.0-alpine3.15

RUN mkdir /app
WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY src .

EXPOSE 5000

CMD ['kops', 'run operator.py --verbose --standalone']


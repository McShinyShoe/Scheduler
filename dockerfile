FROM python:alpine

RUN apk add --no-cache bash

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r src/requirements.txt

EXPOSE 5000

ENV PRODUCTION=false

RUN chmod +x run.sh

CMD  ["python", "src/app.py"]
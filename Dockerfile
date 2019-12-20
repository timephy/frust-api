FROM python:3.8-alpine

WORKDIR /usr/src/app

RUN apk --update add make build-base

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 80

CMD ["python", "."]

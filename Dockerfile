FROM python:alpine3.6

WORKDIR /usr/src/app

RUN apk --update add make build-base

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 80

CMD ["python", "."]

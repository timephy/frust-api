FROM python:alpine3.6

WORKDIR /usr/src/app

RUN apk --update add make build-base

COPY backend/requirements.txt backend/
RUN pip install -r backend/requirements.txt

COPY backend/ backend/
COPY frontend/ frontend/

EXPOSE 80

WORKDIR /usr/src/app/backend/

CMD ["python", "."]

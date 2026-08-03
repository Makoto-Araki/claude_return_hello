FROM python:3.14-alpine

RUN addgroup -S app && adduser -S -G app app

WORKDIR /app
COPY src/hello.py .

USER app

CMD ["python", "hello.py"]

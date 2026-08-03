FROM python:3.14-alpine

WORKDIR /app
COPY src/hello.py .

CMD ["python", "hello.py"]

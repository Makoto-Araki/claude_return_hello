FROM python:3.12-alpine

WORKDIR /app
COPY src/hello.py .

CMD ["python", "hello.py"]

FROM registry-1.docker.io/library/python:3.10-slim


WORKDIR /app

COPY . /app
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]

FROM python:3.11-slim

WORKDIR /app

COPY flask_backend.py .
COPY index.html .

RUN pip install --no-cache-dir flask flask-cors

EXPOSE 5000

CMD ["python", "flask_backend.py"]

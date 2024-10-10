FROM python:3.9-slim

WORKDIR /app

COPY pub.py .env image.jpeg /app/

RUN pip install --upgrade pip \	
    --no-cache-dir \
    six==1.16.0 \
    is-wire==1.2.1 \
    is-msgs==1.1.18 \
    protobuf==3.20.3 \
    opencv-python-headless \
    numpy==1.24.4 \
    python-dotenv

CMD ["python", "pub.py"]
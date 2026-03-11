FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    p7zip-full \
    mame-tools \
    && rm -rf /var/lib/apt/lists/*

RUN pip install py7zr

WORKDIR /app
COPY extract.py .

ENTRYPOINT ["python3", "extract.py"]

# python image
FROM python:3.13.2-slim

# Install dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python3 python3-dev gcc \
    gfortran build-essential libssl-dev libffi-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*


RUN pip install --upgrade pip

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt



COPY . .

CMD ["python", "run.py"]
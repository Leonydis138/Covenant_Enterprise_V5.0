FROM nvidia/cuda:12.1.0-runtime-ubuntu22.04
RUN apt-get update && apt-get install -y python3.11 python3-pip
WORKDIR /app
COPY requirements-full.txt .
RUN pip install --no-cache-dir -r requirements-full.txt
COPY src/ ./src/
CMD ["uvicorn", "covenant.api.ultimate_api:app", "--host", "0.0.0.0", "--port", "8000"]

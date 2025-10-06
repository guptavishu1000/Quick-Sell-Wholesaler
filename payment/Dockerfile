# payment/Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
# Use the --mount flag directly on the RUN instruction
RUN --mount=type=cache,target=/root/.cache/pip pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
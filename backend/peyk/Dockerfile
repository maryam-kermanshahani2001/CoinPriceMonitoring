# Stage 1: Build
FROM python:3.10.12-alpine3.18 AS builder

WORKDIR /app

COPY requirements.txt .

RUN apk add --no-cache gcc musl-dev libffi-dev openssl-dev

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Build the project (replace "peyk:app" with the filename if needed)
RUN python -m compileall -b . && rm -rf __pycache__

# Stage 2: Run
FROM python:3.10.12-alpine3.18

WORKDIR /app

COPY --from=builder /app .

RUN apk --no-cache add libpq

# Install UVicorn and other dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the required port
EXPOSE 8080

# Set the entrypoint command
CMD ["uvicorn", "peyk:app", "--host", "0.0.0.0", "--port", "8080"]

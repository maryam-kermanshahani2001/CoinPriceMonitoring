# Stage 1: Build
FROM python:3.10.12-alpine3.18 AS builder

WORKDIR /app

COPY requirements.txt .

#RUN apk add --no-cache postgresql-dev

RUN pip install -r requirements.txt

# Copy your source code to the container
COPY . /app

# Build the project
#CMD ["python", "/app/bepa.py"]

# Stage 2: Run
FROM python:3.10.12-alpine3.18
WORKDIR /app
COPY --from=builder /app/bepa.py /app
COPY . /app
# Expose any necessary ports
#EXPOSE <7890>
# Define the command to run your application
CMD ["python", "./bepa/bepa.py"]

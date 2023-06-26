# Stage 1: Build
FROM python:3.10.12-alpine3.18 AS builder

WORKDIR /app

COPY requirements.txt .

#RUN apk add --no-cache postgresql-dev

RUN pip install -r requirements.txt

# Copy your source code to the container
COPY . .
#CMD ["/bin/sh"]
# Build the project
#CMD ["python", "/app/bepa.py"]

# Stage 2: Run
FROM python:3.10.12-alpine3.18
COPY --from=builder . .
WORKDIR /app

#COPY . .
# Expose any necessary ports
#EXPOSE <7890>
# Define the command to run your application
CMD ["/bin/sh"]

#CMD ["python", "./bepa/bepa.py"]
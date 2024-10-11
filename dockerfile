# Use Python 3.10 as base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install Rust and Cargo and system dependencies required for Python packages
RUN apt-get update && \
    apt-get install -y curl build-essential && \
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt


# Copy the rest of the application
COPY app.py .

COPY . /app/

# Expose the port the app runs on
EXPOSE 5000

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Command to run the application directly with Python
CMD ["python", "app.py"]
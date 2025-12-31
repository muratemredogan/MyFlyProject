# Use Python 3.9 slim image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src/
COPY tests/ ./tests/
COPY smoke_test.sh ./

# Expose port
EXPOSE 8000

# Set Python path
ENV PYTHONPATH=/app

# Run the application
CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000"]


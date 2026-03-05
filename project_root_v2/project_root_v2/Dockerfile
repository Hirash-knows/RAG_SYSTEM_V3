# Use official Python image
FROM python:3.11

# Set working directory
WORKDIR /app

# Copy dependency file first
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy rest of RAG code
COPY . .

# Start RAG service
CMD ["python", "nats_client.py"]

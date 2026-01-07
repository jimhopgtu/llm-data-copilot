FROM python:3.10-slim

WORKDIR /app

# Install system dependencies needed for ML packages
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy all code
COPY . .

# Install backend requirements (now in /app/backend/)
RUN pip install --no-cache-dir -r /app/backend/requirements.txt

# Move to backend directory
WORKDIR /app/backend

# Create data directories
RUN mkdir -p /app/data/documents /app/chroma_data

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]

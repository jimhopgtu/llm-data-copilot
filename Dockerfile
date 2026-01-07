FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy backend folder specifically
COPY backend/ ./backend/

# Install requirements
RUN pip install --no-cache-dir -r backend/requirements.txt

# Change to backend directory
WORKDIR /app/backend

# Create data directories
RUN mkdir -p data/documents chroma_data

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]

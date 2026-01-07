FROM python:3.10-slim

WORKDIR /app

# Install only essential system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy only backend files
COPY backend/ .

# Install Python packages without cache
RUN pip install --no-cache-dir -r requirements.txt && \
    rm -rf /root/.cache/pip

# Clean up unnecessary files
RUN find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true && \
    find . -type f -name "*.pyc" -delete

# Create data directories
RUN mkdir -p /app/data/documents /app/chroma_data

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]

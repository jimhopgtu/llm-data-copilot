FROM python:3.10-slim

WORKDIR /app

# Copy all code first
COPY . .

# Install backend requirements
RUN pip install --no-cache-dir -r backend/requirements.txt

# Move to backend directory
WORKDIR /app/backend

# Create data directories
RUN mkdir -p /app/data/documents /app/chroma_data

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]

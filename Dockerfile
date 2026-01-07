FROM python:3.10-slim

WORKDIR /app

# Copy everything we need
COPY backend/ ./
COPY data/init_db.py ./data/init_db.py

# Install packages
RUN pip install --no-cache-dir -r requirements.railway.txt && \
    rm -rf /root/.cache

# Initialize database
RUN mkdir -p /app/data/documents && \
    cd /app/data && \
    python init_db.py && \
    ls -la /app/data/

EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]

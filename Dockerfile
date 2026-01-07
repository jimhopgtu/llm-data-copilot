FROM python:3.10-slim

WORKDIR /app

COPY backend/ .
COPY data/init_db.py ./data/

# Use minimal requirements (no ML)
RUN pip install --no-cache-dir -r requirements.railway.txt && \
    rm -rf /root/.cache

# Create data directories and initialize database
RUN mkdir -p /app/data/documents && \
    cd /app/data && \
    python init_db.py

EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]

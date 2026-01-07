FROM python:3.10-slim

WORKDIR /app

# Copy backend code
COPY backend/ .

# Copy data initialization script
COPY data/init_db.py ./data/

# Use minimal requirements
RUN pip install --no-cache-dir -r requirements.railway.txt && \
    rm -rf /root/.cache && \
    mkdir -p /app/data/documents

# Make startup script executable
RUN chmod +x startup.sh

EXPOSE 8000
CMD ["./startup.sh"]

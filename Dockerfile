FROM python:3.10-slim

WORKDIR /app

COPY backend/ .
COPY data/init_db.py ./data/

RUN pip install --no-cache-dir -r requirements.railway.txt && \
    rm -rf /root/.cache && \
    mkdir -p /app/data/documents

EXPOSE 8000
CMD ["python", "startup.py"]

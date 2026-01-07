FROM python:3.10-slim

WORKDIR /app

COPY backend/ .

RUN pip install --no-cache-dir -r requirements.railway.txt && \
    rm -rf /root/.cache && \
    mkdir -p data/documents && \
    python init_db.py && \
    mv sample.db data/

EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]

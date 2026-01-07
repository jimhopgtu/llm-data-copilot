FROM python:3.10-slim

WORKDIR /app

COPY backend/ .

# Use minimal requirements (no ML packages)
RUN pip install --no-cache-dir -r requirements.railway.txt

RUN mkdir -p /app/data/documents

EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]

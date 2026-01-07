FROM python:3.10-slim

WORKDIR /app

# Copy only backend
COPY backend/ .

# Debug: Show size before install
RUN du -sh /app && echo "=== Files copied ===" && ls -lah

# Install packages
RUN pip install --no-cache-dir -r requirements.txt

# Debug: Show size after install
RUN du -sh /app && du -sh /root/.cache 2>/dev/null || echo "No cache" && \
    echo "=== Largest directories ===" && \
    du -sh /usr/local/lib/python3.10/site-packages/* 2>/dev/null | sort -hr | head -20

# Clean everything
RUN rm -rf /root/.cache && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Final size check
RUN du -sh /app && du -sh /usr/local

EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]

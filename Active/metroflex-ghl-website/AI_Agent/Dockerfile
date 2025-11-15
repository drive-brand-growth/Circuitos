FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY *.py .
COPY *.json .

# Expose port
EXPOSE 5001

# Health check (uses PORT variable to match app binding)
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
  CMD curl -f http://localhost:${PORT:-5001}/health || exit 1

# Run with Gunicorn (unified_api_server has all 5 agents)
# Use Railway's PORT env var, fallback to 5001 for local development
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:${PORT:-5001} --workers 2 --timeout 120 unified_api_server:app"]

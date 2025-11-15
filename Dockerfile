# Railway-Compatible Dockerfile for MetroFlex AI Agent
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy AI Agent files
COPY Active/metroflex-ghl-website/AI_Agent/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY Active/metroflex-ghl-website/AI_Agent/ .

# Expose port
EXPOSE 5001

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:5001/health || exit 1

# Start command
CMD ["python", "metroflex_ai_agent_enhanced.py"]

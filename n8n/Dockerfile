# Railway-Compatible n8n Dockerfile
FROM n8nio/n8n:latest

# Set working directory
WORKDIR /home/node

# Expose n8n port
EXPOSE 5678

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:5678/healthz || exit 1

# n8n will start automatically (built into base image)

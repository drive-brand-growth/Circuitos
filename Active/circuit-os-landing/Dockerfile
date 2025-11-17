# Lightweight Docker container for Circuit OS Landing Page
FROM python:3.11-slim

WORKDIR /app

# Copy the landing page
COPY index.html /app/

# Expose port (Railway will set PORT env var)
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python3 -c "import urllib.request; urllib.request.urlopen('http://localhost:8080').read()" || exit 1

# Start HTTP server on Railway's PORT or default to 8080
CMD python3 -m http.server ${PORT:-8080}

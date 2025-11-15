"""
Flask app entry point for Gunicorn
Imports the Flask app from metroflex_ai_agent module
"""
from metroflex_ai_agent import app

# Export app for Gunicorn
__all__ = ['app']





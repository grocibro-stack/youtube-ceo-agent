#!/bin/bash
# YouTube CEO Agent - Development Server Startup
# This script starts the API server on localhost

cd "$(dirname "$0")"

echo
echo "============================================"
echo "YouTube CEO Agent API - Local Development"
echo "============================================"
echo
echo "Server will be available at:"
echo "  http://127.0.0.1:8000"
echo
echo "API Documentation (Swagger):"
echo "  http://127.0.0.1:8000/docs"
echo
echo "Alternative Docs (ReDoc):"
echo "  http://127.0.0.1:8000/redoc"
echo
echo "Press Ctrl+C to stop the server"
echo "============================================"
echo

# Activate venv and start server
source venv/bin/activate
python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload

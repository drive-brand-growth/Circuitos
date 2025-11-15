#!/bin/bash

# MetroFlex Enhanced AI Agent - Local Startup Script

echo "🚀 Starting MetroFlex Enhanced AI Agent (Local Testing)"
echo "============================================================"
echo ""

# Navigate to AI_Agent directory
cd "$(dirname "$0")"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    /usr/bin/python3 -m venv venv  # Use Python 3.9 for ChromaDB compatibility
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install/update dependencies
echo "📥 Installing dependencies..."
pip install openai sentence-transformers chromadb flask flask-cors requests python-dotenv pydantic-settings --quiet

# Check for OpenAI API key
if [ -z "$OPENAI_API_KEY" ]; then
    echo ""
    echo "⚠️  OPENAI_API_KEY not set!"
    echo ""
    echo "Please enter your OpenAI API key (it will be stored temporarily for this session):"
    read -s OPENAI_API_KEY
    export OPENAI_API_KEY
    echo ""
    echo "✅ API key set for this session"
fi

# Check for GHL webhook (optional for testing)
if [ -z "$GHL_LEAD_CAPTURE_WEBHOOK" ]; then
    echo ""
    echo "📝 GHL Lead Capture Webhook not set (optional for local testing)"
    echo "   Leads won't be captured, but agent will still work"
    echo ""
    echo "   To enable lead capture, set: export GHL_LEAD_CAPTURE_WEBHOOK='your-webhook-url'"
    echo ""
fi

# Start the enhanced agent
echo ""
echo "🤖 Starting MetroFlex Enhanced AI Agent..."
echo "============================================================"
echo ""
echo "   📊 Vector database will be built on first start (30 seconds)"
echo "   💬 Chat endpoint: http://localhost:5000/webhook/chat"
echo "   🧪 Test intent:   http://localhost:5000/webhook/test-intent"
echo "   ❤️  Health check:  http://localhost:5000/health"
echo ""
echo "   Press CTRL+C to stop the server"
echo ""
echo "============================================================"
echo ""

# Run the enhanced agent
python3 metroflex_ai_agent_enhanced.py

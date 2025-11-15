#!/bin/bash
# Fix Local Agent Setup Script
# Run this in Warp to diagnose and fix your local agent

set -e

BASE_DIR="/Users/noelpena/Desktop/CircuitOS_Local_Complete_Package"
AGENTFORCE_DIR="$BASE_DIR/Active/agentforce_emulator"
VIRTUAL_AGENTFORCE_DIR="$BASE_DIR/Active/virtual-agentforce"

echo "🔧 Local Agent Fix Script"
echo "=========================="
echo ""

# ============================================
# STEP 1: Check which agent you want to fix
# ============================================
echo "📋 Available local agents:"
echo "   1. agentforce_emulator (Salesforce Agentforce emulator)"
echo "   2. virtual-agentforce (Virtual testing environment)"
echo ""
read -p "Which agent needs fixing? (1 or 2, or 'both'): " AGENT_CHOICE
echo ""

# ============================================
# FIX AGENTFORCE EMULATOR
# ============================================
if [[ "$AGENT_CHOICE" == "1" || "$AGENT_CHOICE" == "both" ]]; then
    echo "🔧 Fixing agentforce_emulator..."
    echo ""
    
    cd "$AGENTFORCE_DIR"
    
    # Check if .env exists
    if [ ! -f ".env" ]; then
        echo "⚠️  Missing .env file - creating from template..."
        cp env.example .env
        echo "✅ Created .env file"
        echo "⚠️  IMPORTANT: Edit .env and add your OPENAI_API_KEY"
        echo ""
    else
        echo "✅ .env file exists"
    fi
    
    # Check if uv is installed
    if ! command -v uv &> /dev/null; then
        echo "⚠️  uv not found - installing..."
        curl -LsSf https://astral.sh/uv/install.sh | sh
        echo "✅ uv installed"
        echo "⚠️  You may need to restart your terminal or run: source ~/.bashrc"
        echo ""
    else
        echo "✅ uv is installed"
    fi
    
    # Install dependencies
    echo "📦 Installing dependencies..."
    if command -v uv &> /dev/null; then
        uv sync
        echo "✅ Dependencies installed"
    else
        echo "⚠️  uv not available, trying pip..."
        pip install -r <(uv pip compile pyproject.toml 2>/dev/null || echo "fastapi uvicorn sqlalchemy langchain langgraph")
    fi
    echo ""
    
    # Check Docker
    echo "🐳 Checking Docker services..."
    if ! docker ps &> /dev/null; then
        echo "⚠️  Docker not running or not installed"
        echo "   Start Docker Desktop and run: docker compose -f docker-compose.local.yml up -d"
    else
        echo "✅ Docker is running"
        
        # Check if services are up
        if ! docker ps | grep -q agentforce-postgres; then
            echo "⚠️  Starting Docker services..."
            docker compose -f docker-compose.local.yml up -d
            echo "⏳ Waiting for services to be ready..."
            sleep 5
            echo "✅ Docker services started"
        else
            echo "✅ Docker services are running"
        fi
    fi
    echo ""
    
    # Check for missing config file
    if [ ! -f "configs/otel-collector-config.yaml" ]; then
        echo "⚠️  Missing otel-collector-config.yaml - creating basic config..."
        mkdir -p configs
        cat > configs/otel-collector-config.yaml << 'EOF'
receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
      http:
        endpoint: 0.0.0.0:4318

exporters:
  logging:
    loglevel: debug

service:
  pipelines:
    traces:
      receivers: [otlp]
      exporters: [logging]
EOF
        echo "✅ Created otel-collector-config.yaml"
    fi
    echo ""
    
    echo "✅ agentforce_emulator setup complete!"
    echo ""
    echo "🚀 To run the agent:"
    echo "   cd $AGENTFORCE_DIR"
    echo "   uv run python cli/run_agent.py --preset weekly"
    echo ""
fi

# ============================================
# FIX VIRTUAL AGENTFORCE
# ============================================
if [[ "$AGENT_CHOICE" == "2" || "$AGENT_CHOICE" == "both" ]]; then
    echo "🔧 Fixing virtual-agentforce..."
    echo ""
    
    cd "$VIRTUAL_AGENTFORCE_DIR"
    
    # Check if .env exists
    if [ ! -f ".env" ]; then
        echo "⚠️  Missing .env file - creating template..."
        cat > .env << 'EOF'
# LLM Provider (openai or anthropic)
LLM_PROVIDER=openai

# OpenAI API Key
OPENAI_API_KEY=sk-your-key-here

# Anthropic API Key (if using anthropic)
ANTHROPIC_API_KEY=sk-ant-your-key-here

# Database URL (SQLite for local dev)
DATABASE_URL=sqlite:///./virtual_agentforce.db
EOF
        echo "✅ Created .env file"
        echo "⚠️  IMPORTANT: Edit .env and add your API keys"
        echo ""
    else
        echo "✅ .env file exists"
    fi
    
    # Check Python virtual environment
    if [ ! -d "venv" ]; then
        echo "📦 Creating Python virtual environment..."
        python3 -m venv venv
        echo "✅ Virtual environment created"
    else
        echo "✅ Virtual environment exists"
    fi
    
    # Activate and install dependencies
    echo "📦 Installing dependencies..."
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    echo "✅ Dependencies installed"
    echo ""
    
    # Initialize database
    echo "🗄️  Initializing database..."
    if [ -f "virtual_agentforce/data/init_db.py" ]; then
        python -m virtual_agentforce.data.init_db
        echo "✅ Database initialized"
    else
        echo "⚠️  init_db.py not found - database may need manual setup"
    fi
    echo ""
    
    echo "✅ virtual-agentforce setup complete!"
    echo ""
    echo "🚀 To run the agent:"
    echo "   cd $VIRTUAL_AGENTFORCE_DIR"
    echo "   source venv/bin/activate"
    echo "   uvicorn virtual_agentforce.main:app --reload"
    echo ""
fi

# ============================================
# FINAL SUMMARY
# ============================================
echo "=========================="
echo "✅ Fix script complete!"
echo ""
echo "📝 Next steps:"
echo "   1. Edit .env files with your API keys"
echo "   2. For agentforce_emulator: Ensure Docker services are running"
echo "   3. Test the agent with the commands shown above"
echo ""
echo "🐛 If you still have issues, check:"
echo "   - API keys are valid in .env files"
echo "   - Docker services are running (for agentforce_emulator)"
echo "   - Python version is 3.12+ (for agentforce_emulator) or 3.10+ (for virtual-agentforce)"
echo ""


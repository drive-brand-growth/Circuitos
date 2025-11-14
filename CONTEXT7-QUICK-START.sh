#!/bin/bash
# Context7 MCP Server Quick Setup
# CircuitOS - Steve Jobs Edition
# © 2025 CircuitOS™

set -e

echo "╔════════════════════════════════════════════════════════════╗"
echo "║  Context7 MCP Server Setup for CircuitOS                  ║"
echo "║  Up-to-Date Code Documentation for AI Assistants          ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Check Node.js version
echo "🔍 Checking Node.js version..."
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js v18+ from https://nodejs.org"
    exit 1
fi

NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 18 ]; then
    echo "❌ Node.js version is too old. Please upgrade to v18 or higher."
    echo "   Current version: $(node -v)"
    exit 1
fi

echo "✅ Node.js $(node -v) detected"
echo ""

# Check if Claude Code is available
echo "🔍 Checking for Claude Code CLI..."
if command -v claude &> /dev/null; then
    echo "✅ Claude Code CLI found"
    CLAUDE_AVAILABLE=true
else
    echo "ℹ️  Claude Code CLI not found. Manual configuration will be shown."
    CLAUDE_AVAILABLE=false
fi
echo ""

# Get API key
echo "════════════════════════════════════════════════════════════"
echo "  Step 1: Get Your FREE Context7 API Key"
echo "════════════════════════════════════════════════════════════"
echo ""
echo "1. Open: https://context7.com/dashboard"
echo "2. Sign up for a FREE account"
echo "3. Copy your API key"
echo ""
read -p "📝 Paste your Context7 API key here: " CONTEXT7_API_KEY

if [ -z "$CONTEXT7_API_KEY" ]; then
    echo "❌ No API key provided. Exiting."
    exit 1
fi

echo ""
echo "✅ API key received"
echo ""

# Add to .env file
echo "════════════════════════════════════════════════════════════"
echo "  Step 2: Saving to .env File"
echo "════════════════════════════════════════════════════════════"
echo ""

if [ -f .env ]; then
    echo "ℹ️  .env file exists. Checking for existing Context7 configuration..."
    if grep -q "CONTEXT7_API_KEY" .env; then
        echo "⚠️  Context7 API key already exists in .env"
        read -p "   Replace existing key? (y/n): " REPLACE
        if [ "$REPLACE" = "y" ] || [ "$REPLACE" = "Y" ]; then
            # Remove old key
            sed -i.bak '/CONTEXT7_API_KEY/d' .env
            echo "CONTEXT7_API_KEY=$CONTEXT7_API_KEY" >> .env
            echo "✅ API key updated in .env"
        else
            echo "ℹ️  Keeping existing key"
        fi
    else
        echo "CONTEXT7_API_KEY=$CONTEXT7_API_KEY" >> .env
        echo "✅ API key added to .env"
    fi
else
    echo "# Context7 MCP Server" > .env
    echo "CONTEXT7_API_KEY=$CONTEXT7_API_KEY" >> .env
    echo "✅ .env file created with API key"
fi

echo ""

# Configure MCP server
echo "════════════════════════════════════════════════════════════"
echo "  Step 3: Configure MCP Server"
echo "════════════════════════════════════════════════════════════"
echo ""

if [ "$CLAUDE_AVAILABLE" = true ]; then
    echo "🚀 Installing Context7 MCP server for Claude Code..."
    echo ""

    # Try remote connection first (easiest)
    echo "Method: Remote connection (recommended)"
    if claude mcp add --transport http context7 https://mcp.context7.com/mcp --header "CONTEXT7_API_KEY: $CONTEXT7_API_KEY"; then
        echo "✅ Context7 MCP server installed successfully!"
    else
        echo "⚠️  Remote connection failed. Trying local installation..."
        if claude mcp add context7 -- npx -y @upstash/context7-mcp --api-key "$CONTEXT7_API_KEY"; then
            echo "✅ Context7 MCP server installed successfully (local)!"
        else
            echo "❌ Installation failed. Please check the error messages above."
            exit 1
        fi
    fi
else
    echo "ℹ️  Manual Configuration Required"
    echo ""
    echo "For Cursor, add this to ~/.cursor/mcp.json:"
    echo ""
    echo "{
  \"mcpServers\": {
    \"context7\": {
      \"url\": \"https://mcp.context7.com/mcp\",
      \"headers\": {
        \"CONTEXT7_API_KEY\": \"$CONTEXT7_API_KEY\"
      }
    }
  }
}"
    echo ""
    echo "For other editors, see: /Docs/CONTEXT7-MCP-SETUP.md"
fi

echo ""

# Test installation
echo "════════════════════════════════════════════════════════════"
echo "  Step 4: Test Your Setup"
echo "════════════════════════════════════════════════════════════"
echo ""
echo "Test Context7 by asking your AI assistant:"
echo ""
echo "  use context7: What's new in React 19?"
echo ""
echo "You should see the AI fetch the latest React 19 documentation."
echo ""

# Show usage examples
echo "════════════════════════════════════════════════════════════"
echo "  Usage Examples for CircuitOS"
echo "════════════════════════════════════════════════════════════"
echo ""
echo "1. Update Virtual LPR with latest Google Maps API:"
echo "   use context7: Refactor Virtual LPR using Google Maps API v3 with TypeScript"
echo ""
echo "2. Build GHL workflows with current API:"
echo "   use context7: Create GHL workflow using GoHighLevel API v2"
echo ""
echo "3. Clone a website with latest stack:"
echo "   use context7: Clone stripe.com using React 19, Next.js 15, and Tailwind CSS v4"
echo ""

# Summary
echo "════════════════════════════════════════════════════════════"
echo "  ✅ Setup Complete!"
echo "════════════════════════════════════════════════════════════"
echo ""
echo "Next Steps:"
echo "1. Test Context7 with the example prompts above"
echo "2. Read the full guide: /Docs/CONTEXT7-MCP-SETUP.md"
echo "3. Start building with up-to-date documentation!"
echo ""
echo "Free Tier Limits:"
echo "  • 100 requests/day (3,000/month)"
echo "  • All public framework documentation"
echo "  • Upgrade at: https://context7.com/pricing"
echo ""
echo "Support:"
echo "  • Documentation: https://context7.com/docs"
echo "  • GitHub: https://github.com/upstash/context7"
echo "  • CircuitOS Guide: /Docs/CONTEXT7-MCP-SETUP.md"
echo ""
echo "Happy coding with always up-to-date documentation! 🚀"
echo ""

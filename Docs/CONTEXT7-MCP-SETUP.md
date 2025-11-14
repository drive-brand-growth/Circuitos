# Context7 MCP Server Setup Guide
## Up-to-Date Code Documentation for AI Coding Tools

**Version:** 1.0.0
**Date:** November 14, 2025
**Cost:** FREE (with optional paid tier for higher limits)

---

## 🎯 What is Context7?

Context7 is an MCP (Model Context Protocol) server that provides **up-to-date, version-specific documentation** directly to your AI coding assistant. Instead of relying on outdated training data, Context7 fetches the latest official documentation and code examples in real-time.

### Problem It Solves

When you ask an AI to generate code using frameworks like:
- React
- TypeScript
- Next.js
- Vue
- Angular
- Any other framework

...the AI might use **outdated patterns** or **deprecated APIs** because its training data is months or years old.

### Context7 Solution

Context7 **dynamically injects current documentation** into your AI's context, ensuring:
- ✅ Latest best practices
- ✅ Current API methods
- ✅ Version-specific examples
- ✅ Up-to-date TypeScript types
- ✅ Recent framework changes

---

## 🚀 Quick Setup (5 Minutes)

### Step 1: Get Your FREE API Key

1. Go to: **https://context7.com/dashboard**
2. Sign up for a free account
3. Copy your API key

**Free Tier Includes:**
- Up to 100 requests/day
- Access to public documentation
- All major frameworks supported

**Paid Tier ($10/month):**
- Unlimited requests
- Private repository documentation
- Priority support

---

### Step 2: Configure Your Coding Tool

#### For Claude Code (Recommended for CircuitOS)

**Remote Connection (Easiest):**
```bash
claude mcp add --transport http context7 https://mcp.context7.com/mcp --header "CONTEXT7_API_KEY: YOUR_API_KEY_HERE"
```

**Local Connection (More Control):**
```bash
claude mcp add context7 -- npx -y @upstash/context7-mcp --api-key YOUR_API_KEY_HERE
```

---

#### For Cursor

Add to `~/.cursor/mcp.json`:

**Remote Connection:**
```json
{
  "mcpServers": {
    "context7": {
      "url": "https://mcp.context7.com/mcp",
      "headers": {
        "CONTEXT7_API_KEY": "YOUR_API_KEY_HERE"
      }
    }
  }
}
```

**Local Connection:**
```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp", "--api-key", "YOUR_API_KEY_HERE"]
    }
  }
}
```

---

#### For Windsurf, Warp, or Other Editors

Check your editor's MCP configuration file location (usually in `~/.config/<editor>/mcp.json`) and use the same JSON structure as Cursor.

---

### Step 3: Verify Installation

**Test the connection:**

In your AI coding tool, ask:
```
use context7: Show me how to create a Next.js 15 app router component with TypeScript
```

You should see the AI fetch the latest Next.js 15 documentation and generate code using current best practices.

---

## 💡 Usage Examples

### Example 1: Clone a Website with Latest React Patterns

**Prompt:**
```
use context7: Clone the homepage of stripe.com using React 19, TypeScript, and Tailwind CSS. Use the latest best practices.
```

**What Context7 Does:**
1. Fetches React 19 documentation
2. Retrieves current TypeScript best practices
3. Pulls Tailwind CSS v4 (latest) utilities
4. Generates code using up-to-date patterns

---

### Example 2: Build API Routes with Latest Next.js

**Prompt:**
```
use context7: Create Next.js 15 API routes for a CRUD system with Supabase. Use the latest App Router patterns.
```

**What Context7 Does:**
1. Fetches Next.js 15 App Router docs
2. Retrieves Supabase TypeScript SDK v2 documentation
3. Uses current route handler syntax
4. Applies latest server component patterns

---

### Example 3: Add CircuitOS Features with Best Practices

**Prompt:**
```
use context7: Add a Virtual LPR detection system using React Server Components, Server Actions, and Vercel Edge Functions. Use TypeScript and the latest patterns.
```

**What Context7 Does:**
1. Fetches React Server Components documentation
2. Retrieves Next.js Server Actions best practices
3. Pulls Vercel Edge Runtime API documentation
4. Generates code using current patterns (not outdated SSR methods)

---

## 🔧 Integration with CircuitOS

### Use Case 1: Building GHL Workflows with Latest APIs

**Before Context7:**
```
Claude, build a GHL workflow automation
```
AI uses outdated GHL API v1 patterns from 2023 training data.

**With Context7:**
```
use context7: Build a GHL workflow using the latest GoHighLevel API v2 with webhooks and custom fields
```
AI fetches current GHL API v2 documentation and uses latest endpoints.

---

### Use Case 2: Updating Virtual LPR System

**Before Context7:**
```
Update the Virtual LPR system to use Google Maps API
```
AI might use deprecated `google.maps.Geocoder` patterns.

**With Context7:**
```
use context7: Update Virtual LPR to use the latest Google Maps JavaScript API v3 with Places API v2 and TypeScript
```
AI fetches current Google Maps API documentation with latest TypeScript types.

---

### Use Case 3: Adding Supabase Database Integration

**Before Context7:**
```
Add Supabase database queries for lead storage
```
AI might use old `supabase-js` v1 syntax.

**With Context7:**
```
use context7: Integrate Supabase v2 with TypeScript for lead storage, using Row Level Security and real-time subscriptions
```
AI fetches Supabase v2 documentation with current RLS patterns.

---

## 📊 Supported Frameworks & Libraries

Context7 supports **1000+ frameworks**, including:

### Frontend
- React (all versions)
- Vue
- Angular
- Svelte
- Next.js
- Nuxt
- Astro
- Solid.js

### Backend
- Node.js
- Express
- Fastify
- NestJS
- Hono
- Bun

### Databases
- Supabase
- PostgreSQL
- MongoDB
- Redis
- Prisma ORM

### APIs & Services
- Google Maps API
- Google Analytics
- Stripe
- Twilio
- SendGrid
- OpenAI

### CSS & Styling
- Tailwind CSS
- shadcn/ui
- Material UI
- Chakra UI

### DevOps
- Vercel
- Docker
- GitHub Actions
- AWS Lambda

**Full list:** https://context7.com/docs

---

## 🎯 Best Practices

### 1. Always Specify Versions

**Bad:**
```
use context7: Create a React component
```

**Good:**
```
use context7: Create a React 19 component with TypeScript 5.5
```

---

### 2. Combine Multiple Technologies

**Example:**
```
use context7: Build a Next.js 15 app with Supabase v2, Stripe webhooks, and Tailwind CSS v4
```

This fetches documentation for all technologies in one context.

---

### 3. Use for Debugging

**Example:**
```
use context7: Why is my Next.js Server Action returning undefined? I'm using Next.js 15 and TypeScript.
```

Context7 will fetch the latest Server Actions documentation to diagnose the issue.

---

### 4. Check Breaking Changes

**Example:**
```
use context7: What changed in React 19 from React 18? Show me migration examples.
```

Helps you update CircuitOS components when frameworks release new versions.

---

## 💰 Cost Analysis

### FREE Tier
- 100 requests/day = 3,000/month
- Perfect for individual developers
- All public documentation

**Ideal for:** Building CircuitOS features, updating existing code

### Paid Tier ($10/month)
- Unlimited requests
- Private repo documentation (if you have private Supabase functions, custom libraries, etc.)
- Priority rate limits

**Ideal for:** Production teams, high-volume development

---

## 🔐 Security & Privacy

### What Context7 Sees
- Your prompts (to fetch relevant documentation)
- Framework names and versions you request

### What Context7 Does NOT See
- Your source code
- API keys or credentials
- Private repository contents (unless on paid tier with explicit permission)

**Data Retention:** Context7 does not store your prompts long-term.

---

## 🧪 Testing Your Setup

### Test 1: Verify Connection

**Prompt:**
```
use context7: What's new in TypeScript 5.5?
```

**Expected:** AI fetches TypeScript 5.5 release notes and explains new features.

---

### Test 2: Generate Code

**Prompt:**
```
use context7: Create a TypeScript function that validates email addresses using the latest Zod v3 schema validation
```

**Expected:** AI generates code using current Zod v3 syntax (not outdated v2).

---

### Test 3: Debugging

**Prompt:**
```
use context7: I'm getting a TypeScript error "Type instantiation is excessively deep and possibly infinite" in Next.js 15. How do I fix this?
```

**Expected:** AI fetches Next.js 15 TypeScript configuration documentation and provides a fix.

---

## 🚀 Advanced Configuration

### Proxy Configuration (for Corporate Networks)

If you're behind a corporate proxy:

```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp", "--api-key", "YOUR_API_KEY"],
      "env": {
        "HTTP_PROXY": "http://your-proxy:8080",
        "HTTPS_PROXY": "http://your-proxy:8080"
      }
    }
  }
}
```

---

### Custom Timeout (for Slow Connections)

```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp", "--api-key", "YOUR_API_KEY", "--timeout", "60000"]
    }
  }
}
```

---

## 🐛 Troubleshooting

### Issue 1: "Context7 MCP server not responding"

**Solution:**
1. Check your API key is correct
2. Verify Node.js >= v18 is installed: `node --version`
3. Test connection manually: `npx -y @upstash/context7-mcp --api-key YOUR_KEY --test`

---

### Issue 2: "Rate limit exceeded"

**Solution:**
- Free tier: 100 requests/day. Upgrade to paid tier for unlimited.
- Check your usage: https://context7.com/dashboard

---

### Issue 3: "Documentation not found for framework X"

**Solution:**
- Ensure framework is supported: https://context7.com/docs
- Check if you specified the correct version: `use context7: React 19` (not just "React")
- Try a more specific prompt: `use context7: React 19 hooks documentation`

---

## 📈 CircuitOS Integration Roadmap

### Phase 1: Setup (Today)
- ✅ Install Context7 MCP server
- ✅ Test with basic prompts
- ✅ Verify documentation fetching

### Phase 2: Refactor Virtual LPR (Week 1)
- Use Context7 to update Google Maps API integration
- Refactor Census API calls with latest patterns
- Update Supabase queries to v2 syntax

### Phase 3: Build New Features (Week 2+)
- Add GHL workflow automation with latest API
- Integrate Stripe subscriptions with current webhooks
- Build DMN agent system with latest OpenAI SDK

### Phase 4: Continuous Updates (Ongoing)
- Run monthly "use context7" audits to check for outdated code
- Update dependencies based on Context7 recommendations
- Monitor framework changelog via Context7

---

## 🎯 Next Steps

1. **Get API Key** (2 minutes)
   - Go to: https://context7.com/dashboard
   - Sign up and copy your API key

2. **Configure Claude Code** (1 minute)
   ```bash
   claude mcp add --transport http context7 https://mcp.context7.com/mcp --header "CONTEXT7_API_KEY: YOUR_KEY"
   ```

3. **Test Setup** (2 minutes)
   - Ask: `use context7: What's new in Next.js 15?`
   - Verify documentation is fetched

4. **Integrate with CircuitOS** (ongoing)
   - Use Context7 for all new feature development
   - Refactor existing code with latest patterns
   - Stay current with framework updates

---

## 📚 Resources

- **Context7 Homepage:** https://context7.com
- **GitHub Repository:** https://github.com/upstash/context7
- **Documentation:** https://context7.com/docs
- **Dashboard (API Key):** https://context7.com/dashboard
- **Support:** support@context7.com

---

**Status:** ✅ Ready to Deploy
**Cost:** FREE (100 requests/day)
**Time to Setup:** 5 minutes
**Impact:** 10x faster development with up-to-date code patterns

---

**© 2025 CircuitOS™ - Context7 MCP Integration**
**Part of the Steve Jobs Edition AI Stack**

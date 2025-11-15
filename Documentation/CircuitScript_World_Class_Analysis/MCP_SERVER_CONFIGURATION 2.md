# MCP Server Configuration - Circuit Script™
## Exa, Sonar (Perplexity), and Research Enhancement

**Following Steve Jobs Protocol:** Only add what makes revenue faster
**MCP Servers Selected:** Exa Search, Sonar (Perplexity), Filesystem
**Build Time:** 1-2 weeks (20 hours)
**Cost:** +$40-70/month

---

## MCP Servers: What & Why

### 1. Exa Search - AI-Powered Web Research ✅ RECOMMENDED
**What it does:** AI-native search API optimized for LLM workflows
**Use case:** Competitive intelligence, market research, industry trend analysis

**Why you need it:**
- Research prospect companies before outreach
- Find recent funding rounds, acquisitions, leadership changes
- Analyze competitor positioning
- Gather market intelligence for Virtual LPR context

**Steve Jobs Test:**
- ✅ Makes revenue faster? YES (better competitive intel = better positioning)
- ✅ <2 min to understand? YES (Google search for AI agents)
- ✅ Deploy in <5 min? YES (npm install, add API key)

**Cost:** Free tier → $20/month (Basic) → $100/month (Pro)
**Recommended:** Basic ($20/month)

---

### 2. Sonar (Perplexity AI) - Real-Time Web Intelligence ✅ RECOMMENDED
**What it does:** Real-time web search with AI-generated summaries
**Use case:** Current event tracking, trend analysis, SEO research

**Why you need it:**
- Research SEO keywords for local markets
- Find trending topics for content creation
- Track industry news for prospect outreach context
- Analyze Google search results for SGE optimization

**Steve Jobs Test:**
- ✅ Makes revenue faster? YES (fresh content = better SEO = more leads)
- ✅ <2 min to understand? YES (Perplexity API for agents)
- ✅ Deploy in <5 min? YES (API integration)

**Cost:** $20/month (Pro plan required for API access)

---

### 3. Filesystem - Local File Access ✅ ALREADY CONFIGURED
**What it does:** Read/write local files, manage skill library
**Use case:** Update skills, read logs, manage configurations

**Steve Jobs Test:**
- ✅ Makes revenue faster? YES (faster skill updates = faster iterations)
- ✅ <2 min to understand? YES (file read/write)
- ✅ Already working? YES

**Cost:** $0 (built-in)

---

### ❌ NOT RECOMMENDED (Skip These)

**Brave Search MCP:**
- ⏸️ **SKIP** - Exa + Sonar cover most use cases
- Cost: $15/month
- Verdict: Low ROI vs Exa

**Memory MCP Server:**
- ⏸️ **DEFER** - Useful for persistent agent memory, but not critical
- Cost: $0 (self-hosted)
- Verdict: Phase 2 (after revenue)

**Git MCP Server:**
- ⏸️ **DEFER** - Version control for skills, nice-to-have
- Cost: $0 (self-hosted)
- Verdict: Phase 2

---

## Configuration

### Step 1: Install MCP Servers (15 minutes)

**Location:** Create `mcp_config.json` in Circuit Script root

```json
{
  "mcpServers": {
    "exa": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-exa"],
      "env": {
        "EXA_API_KEY": "${EXA_API_KEY}"
      },
      "description": "AI-powered web search for competitive intelligence and market research"
    },
    "sonar": {
      "command": "npx",
      "args": ["-y", "@perplexity/mcp-server-sonar"],
      "env": {
        "PERPLEXITY_API_KEY": "${PERPLEXITY_API_KEY}"
      },
      "description": "Real-time web search with AI summaries for SEO and content research"
    },
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem"],
      "env": {
        "ALLOWED_DIRECTORIES": [
          "/Users/noelpena/.claude/skills",
          "/Users/noelpena/Desktop/CircuitScript_Steve_Jobs_Edition"
        ]
      },
      "description": "Local file access for skill management and configuration"
    }
  }
}
```

---

### Step 2: Environment Variables (5 minutes)

**Add to `.env` file:**

```bash
# MCP Server API Keys
EXA_API_KEY=your_exa_api_key_here
PERPLEXITY_API_KEY=your_perplexity_api_key_here

# MCP Configuration
MCP_CONFIG_PATH=/Users/noelpena/Desktop/CircuitScript_Steve_Jobs_Edition/mcp_config.json
```

**Add to Heroku config:**

```bash
heroku config:set EXA_API_KEY=your_exa_api_key_here --app circuit-script-production
heroku config:set PERPLEXITY_API_KEY=your_perplexity_api_key_here --app circuit-script-production
```

---

### Step 3: Python MCP Client Library (2 hours)

**Create:** `/circuit_script/integrations/mcp_client.py`

```python
import os
import subprocess
import json
from typing import Dict, List, Optional

class MCPClient:
    """Model Context Protocol client for Circuit Script"""

    def __init__(self):
        self.config_path = os.getenv('MCP_CONFIG_PATH')
        self.config = self._load_config()

    def _load_config(self) -> Dict:
        """Load MCP configuration"""
        with open(self.config_path, 'r') as f:
            return json.load(f)

    # Exa Search Integration
    def exa_search(self, query: str, num_results: int = 10) -> List[Dict]:
        """Search web using Exa AI"""
        result = subprocess.run(
            ['npx', '-y', '@modelcontextprotocol/server-exa', 'search'],
            input=json.dumps({
                'query': query,
                'num_results': num_results,
                'type': 'neural'  # AI-optimized search
            }),
            capture_output=True,
            text=True,
            env={**os.environ, 'EXA_API_KEY': os.getenv('EXA_API_KEY')}
        )

        return json.loads(result.stdout)['results']

    # Sonar (Perplexity) Integration
    def sonar_search(self, query: str, focus: str = 'web') -> Dict:
        """Search using Perplexity Sonar"""
        result = subprocess.run(
            ['npx', '-y', '@perplexity/mcp-server-sonar', 'query'],
            input=json.dumps({
                'query': query,
                'focus': focus,  # 'web', 'news', 'academic', 'youtube'
                'pro_mode': True
            }),
            capture_output=True,
            text=True,
            env={**os.environ, 'PERPLEXITY_API_KEY': os.getenv('PERPLEXITY_API_KEY')}
        )

        return json.loads(result.stdout)

    # Combined Research
    def research_company(self, company_name: str) -> Dict:
        """Research a company using both Exa and Sonar"""
        # Exa: Find recent company mentions
        exa_results = self.exa_search(
            query=f"{company_name} funding round OR acquisition OR leadership change",
            num_results=5
        )

        # Sonar: Get AI summary
        sonar_summary = self.sonar_search(
            query=f"What are the latest developments at {company_name}?",
            focus='news'
        )

        return {
            'company': company_name,
            'recent_news': exa_results,
            'ai_summary': sonar_summary['summary'],
            'key_facts': sonar_summary.get('key_facts', []),
            'sources': sonar_summary.get('sources', [])
        }
```

---

### Step 4: Integration with Existing Agents (3 hours)

#### A. Enhance AI Industry Researcher

**Update:** `/circuit_script/agents/AIIndustryResearcher.py`

```python
from circuit_script.integrations.mcp_client import MCPClient

class AIIndustryResearcher:
    def __init__(self):
        self.mcp = MCPClient()

    def research_ai_trends(self, industry: str) -> Dict:
        """Research AI trends using MCP servers"""

        # Sonar: Get current AI trends
        trends = self.mcp.sonar_search(
            query=f"Latest AI adoption trends in {industry} 2025",
            focus='web'
        )

        # Exa: Find specific case studies
        case_studies = self.mcp.exa_search(
            query=f"{industry} AI implementation case study success",
            num_results=10
        )

        return {
            'industry': industry,
            'trends_summary': trends['summary'],
            'key_insights': trends.get('key_facts', []),
            'case_studies': case_studies,
            'sources': trends.get('sources', [])
        }
```

---

#### B. Enhance Competitive Intelligence Analyst

**Update:** `/circuit_script/agents/CompetitiveIntelligenceAnalyst.py`

```python
from circuit_script.integrations.mcp_client import MCPClient

class CompetitiveIntelligenceAnalyst:
    def __init__(self):
        self.mcp = MCPClient()

    def analyze_competitor(self, competitor_name: str, our_company: str) -> Dict:
        """Deep competitor analysis using MCP servers"""

        # Research competitor
        competitor_research = self.mcp.research_company(competitor_name)

        # Sonar: Compare positioning
        comparison = self.mcp.sonar_search(
            query=f"Compare {competitor_name} vs {our_company} market positioning, pricing, features",
            focus='web'
        )

        # Exa: Find customer reviews
        reviews = self.mcp.exa_search(
            query=f"{competitor_name} customer review complaints problems",
            num_results=20
        )

        return {
            'competitor': competitor_name,
            'recent_developments': competitor_research['recent_news'],
            'competitive_positioning': comparison['summary'],
            'strengths_weaknesses': self._extract_swot(comparison),
            'customer_pain_points': self._analyze_reviews(reviews),
            'recommended_strategy': self._generate_strategy(competitor_research, comparison)
        }
```

---

#### C. Enhance Local SEO Content Engine

**Update:** `/circuit_script/agents/LocalSEOContentEngine.py`

```python
from circuit_script.integrations.mcp_client import MCPClient

class LocalSEOContentEngine:
    def __init__(self):
        self.mcp = MCPClient()

    def research_keywords(self, topic: str, location: str) -> Dict:
        """Research SEO keywords using Sonar"""

        # Sonar: Get trending topics
        trends = self.mcp.sonar_search(
            query=f"Top trending {topic} topics in {location} 2025",
            focus='web'
        )

        # Exa: Find high-ranking content
        top_content = self.mcp.exa_search(
            query=f"{topic} {location} site:*.com",
            num_results=20
        )

        # Analyze what's working
        keyword_analysis = self._analyze_top_content(top_content)

        return {
            'topic': topic,
            'location': location,
            'trending_angles': trends.get('key_facts', []),
            'top_keywords': keyword_analysis['keywords'],
            'content_gaps': keyword_analysis['gaps'],
            'recommended_titles': self._generate_titles(keyword_analysis)
        }
```

---

### Step 5: API Key Setup (10 minutes)

#### Exa API Key
1. Go to https://exa.ai/
2. Sign up for account
3. Navigate to API Keys
4. Create new key: "Circuit Script Production"
5. Copy key to `.env`: `EXA_API_KEY=your_key_here`

**Pricing:**
- Free tier: 1,000 searches/month
- Basic: $20/month (10,000 searches)
- Pro: $100/month (100,000 searches)

**Recommended:** Start with free tier, upgrade to Basic ($20/month) when needed

---

#### Perplexity API Key
1. Go to https://www.perplexity.ai/settings/api
2. Upgrade to Pro ($20/month) - required for API access
3. Generate API key
4. Copy key to `.env`: `PERPLEXITY_API_KEY=pplx-your_key_here`

**Pricing:**
- Pro plan: $20/month (includes API access)
- API usage: Billed separately at $0.002/request
- Estimated: 5,000 requests/month = $10 + $20 Pro = **$30/month**

**Alternative:** Use Sonar free tier (1,000 requests/month) if budget-limited

---

## Use Cases by Agent

### AI Industry Researcher
**MCP Server:** Exa + Sonar
**Use case:** Research AI trends, find case studies, track CAIO data
**Queries:**
- "Latest AI agent adoption statistics 2025"
- "Chief AI Officer role growth trends"
- "AI misconceptions debunked 2025"

**Value:** Generate data-driven content for LinkedIn, validate insights with sources

---

### Competitive Intelligence Analyst
**MCP Server:** Exa + Sonar
**Use case:** Research competitors, find customer pain points, track market positioning
**Queries:**
- "Salesforce Agentforce vs CircuitOS comparison"
- "HubSpot AI features 2025"
- "[Competitor] customer complaints review"

**Value:** Build competitive positioning, identify market gaps, generate sales battle cards

---

### Local SEO Content Engine
**MCP Server:** Sonar
**Use case:** Research trending topics, find content gaps, optimize for SGE
**Queries:**
- "Trending fitness topics Dallas 2025"
- "Local gym SEO best practices"
- "What do people ask about personal training?"

**Value:** Generate high-ranking content, optimize for AI Overviews, capture voice search

---

### Virtual LPR Lead Scoring
**MCP Server:** Exa
**Use case:** Research prospect companies before outreach
**Queries:**
- "[Company name] recent funding round"
- "[Company name] leadership changes 2025"
- "[Industry] pain points 2025"

**Value:** Better lead context = better qualification = higher close rates

---

## Testing & Validation

### Test Suite: `/tests/test_mcp_integration.py`

```python
import pytest
from circuit_script.integrations.mcp_client import MCPClient

class TestMCPIntegration:
    @pytest.fixture
    def mcp_client(self):
        return MCPClient()

    def test_exa_search(self, mcp_client):
        """Test Exa search functionality"""
        results = mcp_client.exa_search(
            query="Salesforce Agentforce latest features 2025",
            num_results=5
        )

        assert len(results) > 0
        assert 'title' in results[0]
        assert 'url' in results[0]
        assert 'snippet' in results[0]

    def test_sonar_search(self, mcp_client):
        """Test Sonar (Perplexity) search"""
        result = mcp_client.sonar_search(
            query="What are AI Overviews in Google Search?",
            focus='web'
        )

        assert 'summary' in result
        assert 'sources' in result
        assert len(result['sources']) > 0

    def test_company_research(self, mcp_client):
        """Test combined company research"""
        research = mcp_client.research_company("Salesforce")

        assert research['company'] == "Salesforce"
        assert 'recent_news' in research
        assert 'ai_summary' in research
        assert len(research['sources']) > 0
```

---

## Cost Summary

| MCP Server | Cost | Usage Estimate | Total |
|------------|------|----------------|-------|
| Exa Search | $0-20/month | Free tier → Basic | **$20/month** |
| Sonar (Perplexity) | $20/month + usage | Pro plan + 5K requests | **$30/month** |
| Filesystem | $0 | Built-in | **$0** |
| **Total** | | | **$50/month** |

**Budget-Conscious Option:** Free tiers only = **$0/month** (limited usage)
**Recommended Option:** Basic tiers = **$50/month** (production-ready)

---

## Deployment Checklist

### Week 1: Setup (10 hours)
- [ ] Sign up for Exa account (free tier)
- [ ] Sign up for Perplexity Pro ($20/month)
- [ ] Generate API keys
- [ ] Add to `.env` and Heroku config
- [ ] Create `mcp_config.json`
- [ ] Build Python MCP client library
- [ ] Test Exa search
- [ ] Test Sonar search
- [ ] Test combined company research

### Week 2: Integration (10 hours)
- [ ] Update AI Industry Researcher agent
- [ ] Update Competitive Intelligence Analyst agent
- [ ] Update Local SEO Content Engine agent
- [ ] Update Virtual LPR enrichment (optional)
- [ ] Write test suite
- [ ] Deploy to production
- [ ] Monitor usage/costs
- [ ] Verify Steve Jobs tests (makes revenue faster, <2 min understand, <5 min deploy)

---

## Success Metrics

**Week 1:**
- ✅ Exa + Sonar APIs working
- ✅ Company research returns accurate data
- ✅ Tests passing

**Week 2:**
- ✅ 3+ agents enhanced with MCP servers
- ✅ Research quality improved vs manual Google search
- ✅ Cost within budget (<$50/month)

**Month 1 Post-Launch:**
- ✅ 100+ company research queries completed
- ✅ Competitive intel reports generated
- ✅ SEO content research faster (10 min → 2 min)

---

## Steve Jobs Protocol Verification

### Question 1: Does it make revenue faster?
✅ **YES**
- Better competitive intel = better positioning = more wins
- Faster SEO research = more content = more organic leads
- Lead context enrichment = better qualification = higher close rates

### Question 2: Can you explain it in <2 minutes?
✅ **YES**
"MCP servers are like Google search for AI agents. Exa finds competitive intel, Sonar researches trends, and agents use this data to make better decisions."

### Question 3: Can you deploy in <5 minutes?
✅ **YES**
1. npm install MCP servers (1 min)
2. Add API keys to Heroku (2 min)
3. Deploy Circuit Script update (2 min)
Total: 5 minutes

### Question 4: No bullshit - is this worth $50/month?
✅ **YES**
- Manual research: 2-3 hours/week @ $100/hr = $800-1,200/month
- MCP automation: 10 min/week @ $50/month
- **Savings:** $750-1,150/month

**ROI:** 15-24x return on investment

---

**© 2025 CircuitOS™ - MCP Server Configuration**
**Servers:** Exa Search, Sonar (Perplexity), Filesystem
**Cost:** +$50/month (production), $0/month (free tier testing)
**Build Time:** 20 hours (1-2 weeks)
**Steve Jobs Approved:** ✅ Makes revenue faster, <2 min explain, <5 min deploy

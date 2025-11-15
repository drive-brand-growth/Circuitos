# CircuitOS SDK Learning System - Complete Guide

**Your Path to Becoming a World-Class Python SDK Developer**

Version: 1.0
Created: November 2024
Aligned with: University of Michigan Chief Data & AI Officer Curriculum

---

## Table of Contents

1. [Introduction](#introduction)
2. [What You'll Learn](#what-youll-learn)
3. [Learning Path](#learning-path)
4. [System Components](#system-components)
5. [Quick Start (5 Minutes)](#quick-start)
6. [Module Breakdown](#module-breakdown)
7. [Hands-On Exercises](#hands-on-exercises)
8. [Integration with CDAIO Curriculum](#integration-with-cdaio-curriculum)
9. [Prototype SDK Documentation](#prototype-sdk-documentation)
10. [Next Steps](#next-steps)

---

## Introduction

This learning system teaches you how Python SDKs power modern AI-driven automation through:

- **Working Code**: Real, runnable prototypes of GHL/Salesforce SDKs
- **Hands-On Exercises**: 20+ exercises you can execute and modify
- **Autonomous Agent Integration**: Learn how LLMs and agents use SDKs as control panels
- **Industry Best Practices**: Patterns from Prefect, Dagster, Temporal, Airbyte, dbt
- **Your Real Projects**: Applied directly to CircuitOS, GHL workflows, and Salesforce Agentforce

### Why This Matters

**From the video**: "When you think about the Python SDK, don't just think about developers writing code. Think a bigger ecosystem: humans, LLMs and agents, all collaborating through the same interface."

**Your advantage**: You'll learn how to build SDKs that enable:
- **Bulk operations**: Update 1,000 GHL workflows in minutes (vs. days manually)
- **Agent autonomy**: AI agents that build, test, and fix pipelines automatically
- **Competitive moat**: Capabilities your competitors can't replicate

---

## What You'll Learn

### Module 1: SDK Fundamentals
- What is a Python SDK and why it matters
- Architecture patterns: Decorator, Builder, Resource Injection
- Type safety with Pydantic
- Error handling and retry logic

### Module 2: Building Your First SDK
- Project structure and tooling
- HTTP client with authentication
- Resource management (Contacts, Workflows, Campaigns)
- Bulk operations with rate limiting

### Module 3: Workflow Automation
- Decorator-based workflow APIs
- Conditional branching and routing
- Multi-platform deployment (GHL, Salesforce, Zapier)
- Validation and testing

### Module 4: Agent Integration
- LLM-friendly API design
- MCP tools for programmatic discovery
- Autonomous pipeline creation
- Self-healing workflows

### Module 5: Production Systems
- Performance optimization
- Observability and monitoring
- Testing strategies
- Documentation and examples

### Module 6: Advanced Patterns
- ML feedback loops
- Lead scoring engines
- Contact enrichment automation
- Virtual LPR™ detection

---

## Learning Path

### Beginner (Weeks 1-2)
**Goal**: Understand SDK concepts and run your first examples

1. Read: PYTHON_SDK_BEST_PRACTICES_ANALYSIS.md
2. Run: Module 1 exercises (SDK fundamentals)
3. Build: Simple GHL contact manager
4. Test: Create/read/update contacts via SDK

### Intermediate (Weeks 3-4)
**Goal**: Build production-ready workflow automation

1. Read: SDK_DESIGN_QUICK_REFERENCE.md
2. Run: Module 2-3 exercises (workflows and automation)
3. Build: Multi-step campaign orchestration
4. Deploy: Real campaign to your GHL account

### Advanced (Weeks 5-6)
**Goal**: Enable AI agents to use your SDK

1. Read: GHL_SALESFORCE_SDK_IMPLEMENTATION_ROADMAP.md
2. Run: Module 4 exercises (agent integration)
3. Build: Autonomous pipeline agent
4. Test: Agent builds and deploys workflows automatically

### Expert (Weeks 7-8)
**Goal**: Production systems with ML feedback loops

1. Run: Module 5-6 exercises (production and advanced)
2. Build: ML-powered lead scoring engine
3. Deploy: Self-improving campaign optimizer
4. Integrate: Full CircuitOS deployment

---

## System Components

### 1. Prototype SDKs (Working Code)

**Location**: `./SDK_Prototypes/`

- **ghl_sdk/** - GoHighLevel SDK with:
  - Contact management
  - Workflow builder
  - Campaign orchestration
  - Lead scoring integration
  - Webhook handlers

- **salesforce_sdk/** - Salesforce Agentforce SDK with:
  - Agent builder
  - Atlas reasoning engine client
  - SOQL query builder
  - Flow generation
  - Data Cloud connectors

- **circuitos_sdk/** - Unified SDK with:
  - Cross-platform workflow deployment
  - Universal lead scoring
  - Contact enrichment
  - Analytics and reporting
  - Agent framework

### 2. Learning Modules (Interactive Tutorials)

**Location**: `./Learning_Modules/`

Each module contains:
- `README.md` - Lesson content
- `exercises/` - Hands-on coding exercises
- `solutions/` - Complete solutions with explanations
- `tests/` - Automated tests to verify your code

### 3. Hands-On Exercises (20+ Runnable Examples)

**Location**: `./Exercises/`

- Simple exercises (10-20 lines of code)
- Intermediate projects (50-100 lines)
- Advanced systems (200+ lines)
- All exercises have automated tests

### 4. Documentation

**Location**: `./Docs/`

- API reference (auto-generated)
- Design patterns guide
- Best practices checklists
- Integration guides
- Troubleshooting FAQ

### 5. Autonomous Pipeline Agent

**Location**: `./.claude/skills/autonomous-pipeline-agent.md`

A skill that:
- Monitors campaign performance
- Detects underperforming workflows
- Automatically generates fixes
- Deploys updates without human intervention
- Reports results via Slack/email

---

## Quick Start (5 Minutes)

### Step 1: Install Dependencies

```bash
cd /Users/noelpena/Desktop/CircuitOS_Local_Complete_Package

# Install Python SDK learning system
pip install -r SDK_Learning_System/requirements.txt
```

### Step 2: Run Your First Example

```bash
# Module 1, Exercise 1: Create a GHL contact
python SDK_Learning_System/Exercises/01_create_contact.py

# You should see:
# ✅ Contact created: contact_abc123
# ✅ Name: Sarah Johnson
# ✅ Email: sarah@example.com
```

### Step 3: Explore the Prototype SDK

```bash
# Run the GHL SDK demo
python SDK_Prototypes/ghl_sdk/examples/demo.py

# You'll see:
# - Contact creation
# - Workflow building
# - Campaign deployment
# - Lead scoring
```

### Step 4: Start Module 1

```bash
# Open the first learning module
cd SDK_Learning_System/Learning_Modules/Module_01_SDK_Fundamentals
cat README.md
```

---

## Module Breakdown

### Module 1: SDK Fundamentals (Week 1)

**Lessons**:
1. What is a Python SDK?
2. Architecture patterns (Decorator, Builder, DI)
3. Type safety with Pydantic
4. Error handling and retries

**Exercises**:
- Exercise 1.1: Create a simple API client
- Exercise 1.2: Add Pydantic models for type safety
- Exercise 1.3: Implement retry logic
- Exercise 1.4: Build a resource manager

**Project**: Simple GHL contact manager

**Tests**: 10 automated tests to verify understanding

---

### Module 2: Building Your First SDK (Week 2)

**Lessons**:
1. Project structure and tooling
2. HTTP client with authentication
3. Resource management
4. Bulk operations

**Exercises**:
- Exercise 2.1: Set up project structure
- Exercise 2.2: Build authenticated HTTP client
- Exercise 2.3: Implement contact CRUD operations
- Exercise 2.4: Add bulk update functionality

**Project**: Full-featured GHL contact SDK

**Tests**: 15 automated tests

---

### Module 3: Workflow Automation (Week 3)

**Lessons**:
1. Decorator-based workflow APIs
2. Workflow builder pattern
3. Conditional branching
4. Multi-platform deployment

**Exercises**:
- Exercise 3.1: Build workflow with decorators
- Exercise 3.2: Add conditional routing
- Exercise 3.3: Generate GHL workflow JSON
- Exercise 3.4: Deploy to live GHL account

**Project**: Database reactivation campaign

**Tests**: 12 automated tests

---

### Module 4: Agent Integration (Week 4)

**Lessons**:
1. LLM-friendly API design
2. MCP tools for discovery
3. Autonomous pipeline creation
4. Self-healing workflows

**Exercises**:
- Exercise 4.1: Add MCP discovery tools
- Exercise 4.2: Build schema introspection
- Exercise 4.3: Create autonomous agent
- Exercise 4.4: Implement self-healing logic

**Project**: Autonomous campaign optimizer

**Tests**: 8 automated tests

---

### Module 5: Production Systems (Week 5)

**Lessons**:
1. Performance optimization
2. Observability and monitoring
3. Testing strategies
4. Documentation

**Exercises**:
- Exercise 5.1: Add performance profiling
- Exercise 5.2: Implement logging and metrics
- Exercise 5.3: Write comprehensive tests
- Exercise 5.4: Generate API documentation

**Project**: Production-ready SDK deployment

**Tests**: 20 automated tests

---

### Module 6: Advanced Patterns (Week 6)

**Lessons**:
1. ML feedback loops
2. Lead scoring engines
3. Contact enrichment
4. Virtual LPR™ integration

**Exercises**:
- Exercise 6.1: Build scoring engine
- Exercise 6.2: Implement enrichment pipeline
- Exercise 6.3: Add ML feedback loop
- Exercise 6.4: Create Virtual LPR detector

**Project**: Self-improving lead scoring system

**Tests**: 15 automated tests

---

## Hands-On Exercises

### Exercise Categories

**Category A: Fundamentals (Exercises 1-5)**
- Simple API clients
- Pydantic models
- Error handling
- Resource management
- Bulk operations

**Category B: Workflows (Exercises 6-10)**
- Decorator patterns
- Workflow builders
- Conditional routing
- Multi-platform deployment
- Testing workflows

**Category C: Agents (Exercises 11-15)**
- MCP tools
- Schema introspection
- Autonomous creation
- Self-healing
- Performance monitoring

**Category D: Production (Exercises 16-20)**
- Optimization
- Observability
- Testing
- Documentation
- Deployment

### Exercise Structure

Each exercise follows this format:

```
Exercise_XX_Name/
├── README.md           # Exercise instructions
├── starter.py          # Starting code with TODOs
├── solution.py         # Complete solution
├── test_exercise.py    # Automated tests
└── data/               # Sample data (if needed)
```

---

## Integration with CDAIO Curriculum

This SDK learning system maps directly to the University of Michigan Chief Data & AI Officer curriculum:

### UMich Module 1: Data Strategy → SDK Module 1: Fundamentals
**Alignment**: Understanding how data flows through systems

**Skills learned**:
- Data pipeline architecture
- API design patterns
- Type safety and data validation

**Application**: Build SDKs that enforce data strategy via code

---

### UMich Module 2: Data Governance → SDK Module 5: Production
**Alignment**: Ensuring data quality, security, compliance

**Skills learned**:
- Error handling and validation
- Observability and monitoring
- Testing and quality assurance

**Application**: Production-grade SDKs with built-in governance

---

### UMich Module 3: AI/ML Strategy → SDK Module 6: Advanced
**Alignment**: Deploying AI/ML systems at scale

**Skills learned**:
- ML feedback loops
- Model deployment automation
- A/B testing infrastructure

**Application**: SDKs that power AI agents and self-improving systems

---

### UMich Module 4: Technology & Tools → SDK Module 2-3: Building
**Alignment**: Selecting and implementing tools

**Skills learned**:
- SDK architecture patterns
- Integration strategies
- Platform evaluation

**Application**: Build vs. buy decisions for data infrastructure

---

### UMich Module 5: Leadership & Change → SDK Module 4: Agents
**Alignment**: Leading AI transformation

**Skills learned**:
- Agent autonomy and delegation
- Self-healing systems
- Organizational automation

**Application**: AI agents that operate independently, freeing up human leadership

---

## Prototype SDK Documentation

### GHL SDK - Quick Reference

**Installation**:
```bash
pip install -e SDK_Prototypes/ghl_sdk
```

**Basic Usage**:
```python
from ghl_sdk import GHLClient

client = GHLClient(
    api_key="your_api_key",
    location_id="your_location"
)

# Create contact
contact = client.contacts.create(
    first_name="Sarah",
    last_name="Johnson",
    email="sarah@example.com"
)

# Build workflow
from ghl_sdk import WorkflowBuilder

workflow = WorkflowBuilder()
    .name("Welcome Sequence")
    .trigger({"type": "tag_added", "tag": "New Customer"})
    .sendEmail({"template": "welcome_email_1"})
    .wait(3, "days")
    .sendEmail({"template": "welcome_email_2"})
    .build()

# Deploy workflow
deployment = workflow.deploy("GHL", {"apiKey": client.api_key})
print(f"Deployed: {deployment.url}")
```

**Advanced Features**:
```python
# Lead scoring
from ghl_sdk.scoring import ARIScorer

scorer = ARIScorer()
score = scorer.scoreComplete(contact)
# => { total: 178, tier: 'S', breakdown: {...} }

# Contact enrichment
from ghl_sdk.enrichment import ContactEnricher

enricher = ContactEnricher({
    "apolloApiKey": "key",
    "clearbitApiKey": "key"
})

enriched = enricher.enrich("email@example.com")
# => { data: {...}, qualityScore: 87, cost: 0.26 }

# Campaign analytics
analytics = client.campaigns.getAnalytics("campaign_id")
# => { opens: 342, clicks: 89, conversions: 23 }
```

---

### Salesforce SDK - Quick Reference

**Installation**:
```bash
pip install -e SDK_Prototypes/salesforce_sdk
```

**Basic Usage**:
```python
from salesforce_sdk import SalesforceClient

client = SalesforceClient(
    username="user@example.com",
    password="password",
    security_token="token"
)

# Query opportunities
opportunities = client.query(
    "SELECT Id, Name, StageName FROM Opportunity WHERE IsClosed = false"
)

# Build Agentforce agent
from salesforce_sdk import AgentBuilder

agent = AgentBuilder("Lost Opp Reactivation")
    .addDataSource("Opportunity")
    .addAction({"type": "query", "entity": "Opportunity"})
    .setInstructions("Analyze lost opportunities...")
    .deploy()
```

---

### CircuitOS SDK - Quick Reference

**Installation**:
```bash
pip install -e SDK_Prototypes/circuitos_sdk
```

**Basic Usage**:
```python
from circuitos_sdk import CircuitOSClient

client = CircuitOSClient({
    "ghl": {"apiKey": "ghl_key"},
    "salesforce": {"username": "sf_user"}
})

# Cross-platform workflow deployment
workflow = client.workflows.builder()
    .name("Lead Nurture")
    .sendEmail({"template": "nurture_1"})
    .build()

# Deploy to both platforms
client.workflows.deploy(workflow, platforms=["GHL", "Salesforce"])

# Universal lead scoring
score = client.scoring.score(lead, engine="ari")

# Analytics across platforms
analytics = client.analytics.getCrossPlat formMetrics()
```

---

## Next Steps

### Day 1: Orientation
- [ ] Read this README completely
- [ ] Install dependencies
- [ ] Run Quick Start examples
- [ ] Explore prototype SDKs

### Week 1: Fundamentals
- [ ] Complete Module 1 lessons
- [ ] Finish all 4 exercises
- [ ] Pass all automated tests
- [ ] Build simple GHL contact manager

### Week 2: Building
- [ ] Complete Module 2 lessons
- [ ] Finish all 4 exercises
- [ ] Build full-featured GHL SDK
- [ ] Deploy to live GHL account

### Week 3: Workflows
- [ ] Complete Module 3 lessons
- [ ] Build database reactivation campaign
- [ ] Deploy to production
- [ ] Measure performance

### Week 4: Agents
- [ ] Complete Module 4 lessons
- [ ] Build autonomous campaign optimizer
- [ ] Test agent autonomy
- [ ] Deploy self-healing workflows

### Week 5: Production
- [ ] Complete Module 5 lessons
- [ ] Add observability and monitoring
- [ ] Write comprehensive tests
- [ ] Generate documentation

### Week 6: Advanced
- [ ] Complete Module 6 lessons
- [ ] Build ML feedback loop
- [ ] Deploy self-improving system
- [ ] Measure ROI

### Week 7-8: Integration
- [ ] Integrate with CircuitOS
- [ ] Deploy to client accounts
- [ ] Train team on SDK usage
- [ ] Document custom patterns

---

## Resources

### Documentation
- [PYTHON_SDK_BEST_PRACTICES_ANALYSIS.md](./Docs/general/PYTHON_SDK_BEST_PRACTICES_ANALYSIS.md)
- [SDK_DESIGN_QUICK_REFERENCE.md](./Docs/general/SDK_DESIGN_QUICK_REFERENCE.md)
- [GHL_SALESFORCE_SDK_IMPLEMENTATION_ROADMAP.md](./Docs/general/GHL_SALESFORCE_SDK_IMPLEMENTATION_ROADMAP.md)

### Prototype SDKs
- [GHL SDK Documentation](./SDK_Prototypes/ghl_sdk/README.md)
- [Salesforce SDK Documentation](./SDK_Prototypes/salesforce_sdk/README.md)
- [CircuitOS SDK Documentation](./SDK_Prototypes/circuitos_sdk/README.md)

### Learning Modules
- [Module 1: SDK Fundamentals](./SDK_Learning_System/Learning_Modules/Module_01_SDK_Fundamentals/README.md)
- [Module 2: Building Your First SDK](./SDK_Learning_System/Learning_Modules/Module_02_Building_SDK/README.md)
- [Module 3: Workflow Automation](./SDK_Learning_System/Learning_Modules/Module_03_Workflow_Automation/README.md)
- [Module 4: Agent Integration](./SDK_Learning_System/Learning_Modules/Module_04_Agent_Integration/README.md)
- [Module 5: Production Systems](./SDK_Learning_System/Learning_Modules/Module_05_Production_Systems/README.md)
- [Module 6: Advanced Patterns](./SDK_Learning_System/Learning_Modules/Module_06_Advanced_Patterns/README.md)

### Support
- GitHub Issues: Report bugs or request features
- Slack Channel: #circuitos-sdk-learning
- Office Hours: Tuesdays 2-3pm PT

---

## Success Metrics

**By the end of this learning system, you will**:

✅ Understand how Python SDKs power AI automation
✅ Build production-ready SDKs for GHL and Salesforce
✅ Enable AI agents to autonomously manage pipelines
✅ Deploy self-improving, self-healing systems
✅ Reduce manual workflow building time by 95%
✅ Create competitive moats your competitors can't replicate

**Your advantage**: You'll have working code, hands-on experience, and production systems that generate immediate ROI.

---

## License

This learning system is part of the CircuitOS Local Complete Package.
Created: November 2024
Aligned with: University of Michigan Chief Data & AI Officer Curriculum

**Remember**: SDKs aren't just code libraries—they're the control panels that enable humans, LLMs, and agents to collaborate in building the future of AI-driven automation.

Let's build something extraordinary. 🚀

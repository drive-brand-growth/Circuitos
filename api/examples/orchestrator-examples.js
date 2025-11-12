/**
 * Circuit OS - Orchestrator Agent Examples
 *
 * Examples showing how to use the Orchestrator to coordinate
 * multiple Claude agents for complex, multi-step tasks
 */

const API_URL = 'https://your-vercel-url.vercel.app/api/claude-agent-memory';

// ============================================================================
// EXAMPLE 1: Build Complete Lead Nurture System
// ============================================================================

async function example1_BuildCompleteSystem() {
  const response = await fetch(API_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      action: 'orchestrate',
      contactId: 'orchestrator-001',
      businessId: 'my-business-123',
      data: {
        description: `Build a complete lead nurture system for my gym:
          - Score all new GMB leads
          - Generate personalized email and SMS copy based on score
          - Create GHL workflow that automates the entire process
          - Include A/B testing recommendations`,
        context: {
          business: {
            name: 'CrossFit Brooklyn',
            category: 'Fitness',
            location: 'Brooklyn, NY'
          },
          goal: 'Convert 65%+ of high-intent GMB leads',
          constraints: ['TCPA-compliant SMS', 'Budget: $500/mo ad spend']
        },
        useMemory: true
      }
    })
  });

  const result = await response.json();

  console.log('=== ORCHESTRATION PLAN ===');
  console.log(JSON.stringify(result.executionPlan, null, 2));

  console.log('\n=== FULL RESPONSE ===');
  console.log(result.planningResponse);

  // Expected orchestration:
  // 1. Lead Scorer: Analyze typical GMB lead → Define high-intent threshold
  // 2. Copywriter: Generate email sequence (high-intent)
  // 3. Copywriter: Generate SMS sequence (high-intent)
  // 4. Copywriter: Generate email nurture (medium-intent)
  // 5. GHL Workflow Designer: Create complete workflow with all copy
  // 6. Synthesize: Deployment checklist + performance benchmarks
}

// ============================================================================
// EXAMPLE 2: Optimize Existing Workflow
// ============================================================================

async function example2_OptimizeWorkflow() {
  const response = await fetch(API_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      action: 'orchestrate',
      contactId: 'orchestrator-002',
      businessId: 'my-business-123',
      data: {
        description: `Analyze and optimize my current GMB workflow:
          - Currently converting at 35% (goal: 65%)
          - Leads complain about generic messaging
          - SMS open rate is low (28%)`,
        context: {
          currentWorkflow: {
            trigger: 'GMB call/directions',
            steps: [
              'Send generic "Thanks for your interest" email',
              'Wait 24 hours',
              'Send generic follow-up SMS'
            ]
          },
          problems: [
            'Low conversion (35% vs. 65% goal)',
            'Generic messaging',
            'Low SMS open rate (28%)'
          ]
        },
        useMemory: true
      }
    })
  });

  const result = await response.json();

  console.log('=== OPTIMIZATION PLAN ===');
  console.log(JSON.stringify(result.executionPlan, null, 2));

  // Expected orchestration:
  // 1. Lead Scorer: Analyze why conversion is low → Identify missing data
  // 2. Copywriter: Regenerate email with personalization (name, city, distance)
  // 3. Copywriter: Regenerate SMS with higher urgency + time pressure
  // 4. GHL Workflow Designer: Redesign workflow with AI copy + faster timing
  // 5. Synthesize: Before/after comparison + expected lift (+30% conversion)
}

// ============================================================================
// EXAMPLE 3: Create Re-Engagement Campaign
// ============================================================================

async function example3_ReEngagementCampaign() {
  const response = await fetch(API_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      action: 'orchestrate',
      contactId: 'orchestrator-003',
      businessId: 'my-business-123',
      data: {
        description: 'Create a re-engagement campaign for 500 leads who went cold after initial contact',
        context: {
          leads: {
            count: 500,
            originalScore: '70-85',
            lastContact: '30-90 days ago',
            originalChannel: 'email'
          },
          goal: 'Re-engage 15%+ (75 leads)'
        },
        useMemory: true
      }
    })
  });

  const result = await response.json();

  console.log('=== RE-ENGAGEMENT PLAN ===');
  console.log(JSON.stringify(result.executionPlan, null, 2));

  // Expected orchestration:
  // 1. Lead Scorer: Re-score dormant leads (have they visited GMB recently?)
  // 2. Copywriter: Generate Soap Opera Sequence (5 emails, story-driven)
  // 3. GHL Workflow Designer: Create tag-based trigger workflow
  // 4. Synthesize: Implementation checklist + performance tracking
}

// ============================================================================
// EXAMPLE 4: Handle Negative Reviews
// ============================================================================

async function example4_ReviewCrisisManagement() {
  const response = await fetch(API_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      action: 'orchestrate',
      contactId: 'orchestrator-004',
      businessId: 'my-business-123',
      data: {
        description: 'We got 3 negative reviews this week about poor customer service. Create a crisis response plan.',
        context: {
          reviews: [
            { rating: 1, text: 'Rude staff, waited 30 minutes' },
            { rating: 2, text: 'Called 3 times, no answer' },
            { rating: 1, text: 'Charged wrong amount, refused refund' }
          ],
          urgency: 'HIGH'
        },
        useMemory: true
      }
    })
  });

  const result = await response.json();

  console.log('=== CRISIS RESPONSE PLAN ===');
  console.log(JSON.stringify(result.executionPlan, null, 2));

  // Expected orchestration:
  // 1. Reputation Guardian: Draft responses for each review
  // 2. Copywriter: Create internal email to staff about customer service
  // 3. Copywriter: Create "We've improved" email to past customers
  // 4. GHL Workflow Designer: Create review request workflow (get positive reviews)
  // 5. Synthesize: Crisis response playbook + prevention strategies
}

// ============================================================================
// EXAMPLE 5: Launch New Service
// ============================================================================

async function example5_LaunchNewService() {
  const response = await fetch(API_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      action: 'orchestrate',
      contactId: 'orchestrator-005',
      businessId: 'my-business-123',
      data: {
        description: `Launch new "Virtual Training" service:
          - Target existing members + past leads
          - Price: $49/month (vs. $150 in-person)
          - Create complete launch campaign`,
        context: {
          service: {
            name: 'Virtual Training',
            price: 49,
            target: 'Existing members + past leads'
          },
          audiences: {
            existingMembers: 250,
            pastLeads: 1200
          }
        },
        useMemory: true
      }
    })
  });

  const result = await response.json();

  console.log('=== LAUNCH PLAN ===');
  console.log(JSON.stringify(result.executionPlan, null, 2));

  // Expected orchestration:
  // 1. Lead Scorer: Score past leads for re-engagement potential
  // 2. Copywriter: Generate launch announcement (existing members)
  // 3. Copywriter: Generate re-engagement offer (past leads)
  // 4. GHL Workflow Designer: Create segmented launch workflows
  // 5. Synthesize: Launch timeline + revenue projections
}

// ============================================================================
// EXAMPLE 6: Multi-Location Expansion
// ============================================================================

async function example6_MultiLocationExpansion() {
  const response = await fetch(API_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      action: 'orchestrate',
      contactId: 'orchestrator-006',
      businessId: 'my-business-123',
      data: {
        description: `We're opening a second location. Create a system to:
          - Route leads to correct location based on proximity
          - Customize messaging per location
          - Track performance separately`,
        context: {
          locations: [
            { name: 'Brooklyn', address: '123 Main St', open: true },
            { name: 'Queens', address: '456 Park Ave', open: 'opening in 2 weeks' }
          ]
        },
        useMemory: true
      }
    })
  });

  const result = await response.json();

  console.log('=== MULTI-LOCATION PLAN ===');
  console.log(JSON.stringify(result.executionPlan, null, 2));

  // Expected orchestration:
  // 1. Lead Scorer: Add location-based routing logic to Virtual LPR
  // 2. Copywriter: Generate location-specific copy templates
  // 3. GHL Workflow Designer: Create location router workflow
  // 4. Synthesize: Implementation guide + performance tracking per location
}

// ============================================================================
// EXAMPLE 7: Conversational Iteration (Memory in Action)
// ============================================================================

async function example7_ConversationalIteration() {
  // Request 1: Initial ask
  const response1 = await fetch(API_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      action: 'orchestrate',
      contactId: 'orchestrator-007', // SAME ID across requests
      businessId: 'my-business-123',
      data: {
        description: 'Help me improve my lead conversion',
        context: {
          currentConversion: '35%',
          goal: '65%'
        },
        useMemory: true
      }
    })
  });

  const result1 = await response1.json();
  console.log('=== INITIAL PLAN ===');
  console.log(result1.planningResponse);

  // Request 2: Refinement (Orchestrator remembers!)
  const response2 = await fetch(API_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      action: 'orchestrate',
      contactId: 'orchestrator-007', // SAME ID
      businessId: 'my-business-123',
      data: {
        description: 'Actually, I also want to reduce my cost-per-lead. Can you adjust the plan?',
        context: {
          currentCPL: '$45',
          targetCPL: '$25'
        },
        useMemory: true
      }
    })
  });

  const result2 = await response2.json();
  console.log('\n=== REFINED PLAN ===');
  console.log(result2.planningResponse);

  // Request 3: Implementation question
  const response3 = await fetch(API_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      action: 'orchestrate',
      contactId: 'orchestrator-007', // SAME ID
      businessId: 'my-business-123',
      data: {
        description: 'Sounds good. What should I implement first?',
        useMemory: true
      }
    })
  });

  const result3 = await response3.json();
  console.log('\n=== PRIORITIZED IMPLEMENTATION ===');
  console.log(result3.planningResponse);

  // The Orchestrator maintains context across all 3 requests!
}

// ============================================================================
// RUNNING THE EXAMPLES
// ============================================================================

async function runAllExamples() {
  console.log('========================================');
  console.log('ORCHESTRATOR AGENT EXAMPLES');
  console.log('========================================\n');

  await example1_BuildCompleteSystem();
  console.log('\n\n');

  await example2_OptimizeWorkflow();
  console.log('\n\n');

  await example3_ReEngagementCampaign();
  console.log('\n\n');

  await example4_ReviewCrisisManagement();
  console.log('\n\n');

  await example5_LaunchNewService();
  console.log('\n\n');

  await example6_MultiLocationExpansion();
  console.log('\n\n');

  await example7_ConversationalIteration();
}

// Uncomment to run:
// runAllExamples();

export {
  example1_BuildCompleteSystem,
  example2_OptimizeWorkflow,
  example3_ReEngagementCampaign,
  example4_ReviewCrisisManagement,
  example5_LaunchNewService,
  example6_MultiLocationExpansion,
  example7_ConversationalIteration
};

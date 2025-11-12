/**
 * Circuit OS - GHL Workflow Designer Examples
 *
 * Examples showing how to use the AI Workflow Designer
 * to create production-ready GHL workflows
 */

const API_URL = 'https://your-vercel-url.vercel.app/api/claude-agent-memory';

// ============================================================================
// EXAMPLE 1: Design High-Intent GMB Workflow
// ============================================================================

async function example1_HighIntentGMBWorkflow() {
  const response = await fetch(API_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      action: 'design-workflow',
      contactId: 'designer-session-001',
      businessId: 'my-business-123',
      useMemory: true,
      data: {
        description: 'Build a workflow for leads who clicked GMB directions and scored 85+',
        useCase: 'Convert high-intent GMB leads with immediate SMS + email follow-up',
        targetAudience: 'Local service business leads (gyms, restaurants, salons)',
        channel: 'multi-channel', // email, sms, call
        includeAI: true, // Use Claude agents (Lead Scorer, Copywriter)
        complianceLevel: 'full' // TCPA-compliant
      }
    })
  });

  const result = await response.json();

  console.log('=== WORKFLOW DESIGN ===');
  console.log(JSON.stringify(result.workflow, null, 2));
  console.log('\n=== SETUP INSTRUCTIONS ===');
  console.log(result.workflow.ghl_setup_instructions.join('\n'));
}

// ============================================================================
// EXAMPLE 2: Re-Engagement Campaign for Cold Leads
// ============================================================================

async function example2_ReEngagementCampaign() {
  const response = await fetch(API_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      action: 'design-workflow',
      contactId: 'designer-session-002',
      businessId: 'my-business-123',
      useMemory: true,
      data: {
        description: 'Create a re-engagement campaign for leads who haven\'t responded in 30+ days',
        useCase: 'Win back cold leads with Soap Opera Sequence (story-driven emails)',
        targetAudience: 'Previously scored 70+, now dormant',
        channel: 'email',
        includeAI: true,
        complianceLevel: 'basic'
      }
    })
  });

  const result = await response.json();

  console.log('=== RE-ENGAGEMENT WORKFLOW ===');
  console.log(JSON.stringify(result.workflow, null, 2));
}

// ============================================================================
// EXAMPLE 3: Appointment No-Show Follow-Up
// ============================================================================

async function example3_NoShowFollowUp() {
  const response = await fetch(API_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      action: 'design-workflow',
      contactId: 'designer-session-003',
      businessId: 'my-business-123',
      useMemory: true,
      data: {
        description: 'Follow up with leads who booked but didn\'t show up for appointment',
        useCase: 'Recover no-shows with empathetic SMS + reschedule offer',
        targetAudience: 'Appointment no-shows from last 7 days',
        channel: 'sms',
        includeAI: true,
        complianceLevel: 'full'
      }
    })
  });

  const result = await response.json();

  console.log('=== NO-SHOW WORKFLOW ===');
  console.log(JSON.stringify(result.workflow, null, 2));
}

// ============================================================================
// EXAMPLE 4: Tripwire Ascension Sequence
// ============================================================================

async function example4_TripwireAscension() {
  const response = await fetch(API_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      action: 'design-workflow',
      contactId: 'designer-session-004',
      businessId: 'my-business-123',
      useMemory: true,
      data: {
        description: 'Ascend $7 ebook buyers to $97 course',
        useCase: 'Tripwire sequence: low-ticket → high-ticket upsell',
        targetAudience: 'Recent $7 ebook purchasers (last 48 hours)',
        channel: 'email',
        includeAI: true,
        complianceLevel: 'basic'
      }
    })
  });

  const result = await response.json();

  console.log('=== TRIPWIRE WORKFLOW ===');
  console.log(JSON.stringify(result.workflow, null, 2));
}

// ============================================================================
// EXAMPLE 5: Multi-Agent Workflow (Full Stack)
// ============================================================================

async function example5_FullStackWorkflow() {
  // This example shows a workflow that uses ALL agents:
  // Lead Scorer → Copywriter → Channel Router → Workflow Designer

  const response = await fetch(API_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      action: 'design-workflow',
      contactId: 'designer-session-005',
      businessId: 'my-business-123',
      useMemory: true,
      data: {
        description: `Create a complete lead nurture system that:
          1. Scores every new lead with Virtual LPR
          2. Routes high-intent (85+) to immediate SMS
          3. Routes medium-intent (70-84) to email nurture sequence
          4. Generates AI copy for each channel
          5. Tracks outcomes and feeds back to ML system`,
        useCase: 'Complete AI-powered lead nurture automation',
        targetAudience: 'All new leads (local service business)',
        channel: 'multi-channel',
        includeAI: true,
        complianceLevel: 'full'
      }
    })
  });

  const result = await response.json();

  console.log('=== FULL STACK WORKFLOW ===');
  console.log(JSON.stringify(result.workflow, null, 2));

  // The workflow will include:
  // - Trigger: New contact created
  // - Step 1: Call Lead Scorer API (with Virtual LPR data)
  // - Step 2: Conditional branching by score
  // - Step 3: Call Copywriter API for each branch
  // - Step 4: Send messages via appropriate channels
  // - Step 5: Wait periods + engagement tracking
  // - Step 6: Feedback loop (record-feedback action)
}

// ============================================================================
// EXAMPLE 6: Iterative Workflow Design (Using Memory)
// ============================================================================

async function example6_IterativeDesign() {
  // First request: Initial design
  const response1 = await fetch(API_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      action: 'design-workflow',
      contactId: 'designer-session-006', // Same contactId for memory
      businessId: 'my-business-123',
      useMemory: true,
      data: {
        description: 'Create an email nurture sequence for new leads',
        useCase: 'Indoctrination sequence',
        targetAudience: 'New email subscribers',
        channel: 'email',
        includeAI: true,
        complianceLevel: 'basic'
      }
    })
  });

  const result1 = await response1.json();
  console.log('=== INITIAL DESIGN ===');
  console.log(result1.workflow.workflow_name);

  // Second request: Refinement (Designer remembers the first design!)
  const response2 = await fetch(API_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      action: 'design-workflow',
      contactId: 'designer-session-006', // SAME contactId
      businessId: 'my-business-123',
      useMemory: true,
      data: {
        description: 'Modify the previous workflow to add SMS follow-up for high-engagement leads',
        useCase: 'Enhanced indoctrination with SMS escalation',
        targetAudience: 'New subscribers who open 2+ emails',
        channel: 'multi-channel',
        includeAI: true,
        complianceLevel: 'full'
      }
    })
  });

  const result2 = await response2.json();
  console.log('\n=== REFINED DESIGN ===');
  console.log(result2.workflow.workflow_name);

  // The designer will reference the previous workflow and enhance it!
}

// ============================================================================
// EXAMPLE 7: A/B Test Workflow Design
// ============================================================================

async function example7_ABTestWorkflow() {
  const response = await fetch(API_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      action: 'design-workflow',
      contactId: 'designer-session-007',
      businessId: 'my-business-123',
      useMemory: true,
      data: {
        description: 'Create A/B test for email subject lines - test curiosity vs. benefit-driven',
        useCase: 'Optimize email open rates',
        targetAudience: 'New leads scoring 70+',
        channel: 'email',
        includeAI: true,
        complianceLevel: 'basic'
      }
    })
  });

  const result = await response.json();

  console.log('=== A/B TEST WORKFLOW ===');
  console.log(JSON.stringify(result.workflow, null, 2));

  // Will include A/B split logic with two variants
}

// ============================================================================
// RUNNING THE EXAMPLES
// ============================================================================

async function runAllExamples() {
  console.log('========================================');
  console.log('GHL WORKFLOW DESIGNER EXAMPLES');
  console.log('========================================\n');

  await example1_HighIntentGMBWorkflow();
  console.log('\n\n');

  await example2_ReEngagementCampaign();
  console.log('\n\n');

  await example3_NoShowFollowUp();
  console.log('\n\n');

  await example4_TripwireAscension();
  console.log('\n\n');

  await example5_FullStackWorkflow();
  console.log('\n\n');

  await example6_IterativeDesign();
  console.log('\n\n');

  await example7_ABTestWorkflow();
}

// Uncomment to run:
// runAllExamples();

export {
  example1_HighIntentGMBWorkflow,
  example2_ReEngagementCampaign,
  example3_NoShowFollowUp,
  example4_TripwireAscension,
  example5_FullStackWorkflow,
  example6_IterativeDesign,
  example7_ABTestWorkflow
};

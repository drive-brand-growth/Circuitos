/**
 * Multi-Agent Workflow Example
 * Demonstrates ADK-level agent collaboration with shared memory
 *
 * Scenario: Lead comes in → Score → Generate Copy → Send Email → Track Outcome
 */

const VERCEL_API_URL = process.env.VERCEL_API_URL || 'https://your-project.vercel.app';

/**
 * Example 1: Sequential Multi-Agent Workflow
 * Lead Scorer → Copywriter → Email Sent
 */
async function sequentialWorkflow() {
  const contactId = 'contact-' + Date.now();
  const businessId = 'business-crossfit-brooklyn';

  console.log('🚀 Starting Multi-Agent Workflow for', contactId);
  console.log('━'.repeat(60));

  // STEP 1: Lead Scorer Agent
  console.log('\n📊 STEP 1: Lead Scorer Agent');
  console.log('─'.repeat(60));

  const scoringResponse = await fetch(`${VERCEL_API_URL}/api/claude-agent-memory`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      action: 'score-lead',
      contactId,
      businessId,
      useMemory: true,
      data: {
        contact: {
          first_name: 'Sarah',
          last_name: 'Johnson',
          email: 'sarah.johnson@example.com',
          city: 'Brooklyn',
          state: 'NY',
          custom_fields: {
            distance_miles: '0.8',
            median_income: '85000',
            intent_signal: 'GMB_DIRECTIONS_CLICKED',
            neighborhood: 'Williamsburg',
            vlpr_source: 'google_my_business'
          }
        },
        business: {
          name: 'CrossFit Brooklyn',
          category: 'Fitness',
          location: '123 Main St, Brooklyn NY 11211'
        }
      }
    })
  });

  const scoringResult = await scoringResponse.json();
  console.log('✅ Lead Scored:', scoringResult.total_score, '/', 100);
  console.log('   Grade:', scoringResult.grade);
  console.log('   Priority:', scoringResult.priority);
  console.log('   Next Action:', scoringResult.next_action);
  console.log('   Conversation Turns:', scoringResult.metadata.conversationTurns);

  // STEP 2: Copywriter Agent (reads Lead Scorer's context!)
  console.log('\n✍️  STEP 2: Copywriter Agent');
  console.log('─'.repeat(60));
  console.log('   (Agent will see Lead Scorer\'s analysis in conversation history)');

  const copyResponse = await fetch(`${VERCEL_API_URL}/api/claude-agent-memory`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      action: 'generate-copy',
      contactId, // SAME contactId - shared memory!
      businessId,
      useMemory: true,
      data: {
        contact: {
          first_name: 'Sarah',
          last_name: 'Johnson',
          city: 'Brooklyn'
        },
        channel: 'EMAIL',
        awareness_level: 'Solution Aware',
        business: {
          name: 'CrossFit Brooklyn',
          category: 'Fitness'
        }
      }
    })
  });

  const copyResult = await copyResponse.json();
  console.log('✅ Copy Generated:', copyResult.variants.length, 'variants');
  console.log('   Variant A Subject:', copyResult.variants[0].subject);
  console.log('   Conversation Turns:', copyResult.metadata.conversationTurns);
  console.log('   (Agent saw', copyResult.metadata.conversationTurns - 1, 'previous turn(s))');

  // STEP 3: Get Conversation Summary
  console.log('\n📝 STEP 3: Conversation Summary');
  console.log('─'.repeat(60));

  const summaryResponse = await fetch(`${VERCEL_API_URL}/api/claude-agent-memory`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      action: 'get-summary',
      contactId,
      businessId
    })
  });

  const summary = await summaryResponse.json();
  console.log('✅ Summary:', JSON.stringify(summary, null, 2));

  // STEP 4: Simulate sending email and tracking outcome
  console.log('\n📧 STEP 4: Email Sent (simulated)');
  console.log('─'.repeat(60));
  console.log('   Sending variant A to sarah.johnson@example.com...');
  console.log('   Waiting 24 hours for response...');
  console.log('   (In production, this would be tracked by GHL)');

  // STEP 5: Record feedback (24 hours later)
  console.log('\n📈 STEP 5: Record ML Feedback');
  console.log('─'.repeat(60));
  console.log('   (Simulating: lead responded and booked a class)');

  const feedbackResponse = await fetch(`${VERCEL_API_URL}/api/claude-agent-memory`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      action: 'record-feedback',
      contactId,
      businessId,
      data: {
        conversationId: 'conv-' + contactId,
        predicted: 'HIGH_INTENT', // What Lead Scorer predicted
        actual: 'CONVERTED', // What actually happened
        learnedPatterns: {
          signals: ['GMB_DIRECTIONS', 'PROXIMITY_<1MI', 'HIGH_INCOME'],
          worked: true,
          industry: 'fitness',
          copy_variant: 'A'
        }
      }
    })
  });

  const feedback = await feedbackResponse.json();
  console.log('✅ Feedback Recorded:', feedback.success);
  console.log('   (System will use this to improve future predictions)');

  console.log('\n🎉 Workflow Complete!');
  console.log('━'.repeat(60));
  console.log('\nKey Insights:');
  console.log('✓ Lead Scorer and Copywriter shared conversation memory');
  console.log('✓ Copywriter saw Lead Scorer\'s analysis (no manual data passing)');
  console.log('✓ ML feedback loop recorded actual outcome vs prediction');
  console.log('✓ System will learn: GMB directions + proximity = high conversion');
}

/**
 * Example 2: Multi-Turn Conversation with Same Agent
 * Shows how an agent can have a back-and-forth conversation
 */
async function multiTurnConversation() {
  const contactId = 'contact-multiturn-' + Date.now();
  const businessId = 'business-test';

  console.log('\n\n🔄 Multi-Turn Conversation Example');
  console.log('━'.repeat(60));

  // Turn 1: Initial scoring
  console.log('\n🔄 Turn 1: Initial lead scoring (limited data)');
  const turn1 = await fetch(`${VERCEL_API_URL}/api/claude-agent-memory`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      action: 'score-lead',
      contactId,
      businessId,
      useMemory: true,
      data: {
        contact: {
          first_name: 'Mike',
          city: 'Manhattan'
          // Limited data on purpose
        },
        business: {
          name: 'Tech Gym',
          category: 'Fitness'
        }
      }
    })
  });

  const result1 = await turn1.json();
  console.log('   Score:', result1.total_score, '(limited data)');
  console.log('   Missing Data:', result1.missing_data.join(', '));

  // Turn 2: Add more data, re-score
  console.log('\n🔄 Turn 2: Re-score with additional data (agent remembers turn 1)');
  const turn2 = await fetch(`${VERCEL_API_URL}/api/claude-agent-memory`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      action: 'score-lead',
      contactId, // SAME contact - agent remembers!
      businessId,
      useMemory: true,
      data: {
        contact: {
          first_name: 'Mike',
          city: 'Manhattan',
          custom_fields: {
            distance_miles: '2.1',
            median_income: '120000',
            intent_signal: 'WEBSITE_VISIT_3X'
          }
        },
        business: {
          name: 'Tech Gym',
          category: 'Fitness'
        }
      }
    })
  });

  const result2 = await turn2.json();
  console.log('   Score:', result2.total_score, '(much better!)');
  console.log('   Conversation Turns:', result2.metadata.conversationTurns);
  console.log('   Agent saw', result2.metadata.conversationTurns - 1, 'previous scoring(s)');
}

/**
 * Example 3: Parallel Agent Execution (No Memory Sharing)
 * Useful when agents don't need to collaborate
 */
async function parallelAgents() {
  const contactId1 = 'contact-parallel-1-' + Date.now();
  const contactId2 = 'contact-parallel-2-' + Date.now();
  const businessId = 'business-test';

  console.log('\n\n⚡ Parallel Agent Execution Example');
  console.log('━'.repeat(60));
  console.log('   (Processing 2 different leads simultaneously)');

  const [result1, result2] = await Promise.all([
    // Lead 1: Score
    fetch(`${VERCEL_API_URL}/api/claude-agent-memory`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        action: 'score-lead',
        contactId: contactId1,
        businessId,
        useMemory: true,
        data: {
          contact: { first_name: 'Alice', city: 'Brooklyn' },
          business: { name: 'Gym A', category: 'Fitness' }
        }
      })
    }).then(r => r.json()),

    // Lead 2: Score (different contact)
    fetch(`${VERCEL_API_URL}/api/claude-agent-memory`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        action: 'score-lead',
        contactId: contactId2,
        businessId,
        useMemory: true,
        data: {
          contact: { first_name: 'Bob', city: 'Queens' },
          business: { name: 'Gym A', category: 'Fitness' }
        }
      })
    }).then(r => r.json())
  ]);

  console.log('✅ Lead 1 Score:', result1.total_score);
  console.log('✅ Lead 2 Score:', result2.total_score);
  console.log('   (Processed in parallel, isolated memory)');
}

/**
 * Run all examples
 */
async function runAllExamples() {
  try {
    // Example 1: Sequential multi-agent workflow (most common)
    await sequentialWorkflow();

    // Example 2: Multi-turn with same agent
    await multiTurnConversation();

    // Example 3: Parallel execution
    await parallelAgents();

    console.log('\n\n✅ All Examples Complete!');
    console.log('━'.repeat(60));
    console.log('\nCheck your Supabase dashboard to see:');
    console.log('- conversation_history table (all agent interactions)');
    console.log('- agent_feedback table (ML learning data)');
    console.log('- ml_retraining_queue table (flagged for improvement)');

  } catch (error) {
    console.error('❌ Error running examples:', error);
    console.error('   Make sure VERCEL_API_URL is set correctly');
  }
}

// Run if executed directly
if (import.meta.url === `file://${process.argv[1]}`) {
  runAllExamples();
}

export { sequentialWorkflow, multiTurnConversation, parallelAgents };

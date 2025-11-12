/**
 * Complete Sales System Examples
 *
 * Demonstrates the full lead-to-conversion-to-retention workflow using:
 * 1. Lead Validation Agent (12 frameworks)
 * 2. SDR Agent (Eugene Schwartz + Brunson + StoryBrand + Hormozi)
 * 3. Conversation Agent (two-way dialogue)
 * 4. Retention & Growth Agent (churn prevention)
 *
 * All agents share conversational memory and collaborate seamlessly.
 */

const API_URL = 'https://your-vercel-url.vercel.app/api/claude-agent-memory';

// ==================================================
// EXAMPLE 1: HIGH-INTENT GMB LEAD (Complete Flow)
// ==================================================

async function example1_HighIntentGMBLead() {
  console.log('\n=== EXAMPLE 1: High-Intent GMB Lead (Complete Flow) ===\n');

  const contactId = 'lead-gmb-001';
  const businessId = 'gym-brooklyn-01';

  // STEP 1: VALIDATE LEAD (12 Frameworks)
  console.log('STEP 1: Validating lead with 12 sales frameworks...\n');

  const validation = await fetch(API_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      action: 'validate-lead',
      contactId,
      businessId,
      useMemory: true,
      data: {
        // Lead info
        name: 'John Smith',
        email: 'john.smith@techcorp.com',
        phone: '555-0123',
        company: 'TechCorp',
        title: 'VP of Sales',

        // BANT signals
        budget: {
          allocated: true,
          amount: '$50,000',
          fiscal_year: 'Q4 2025'
        },
        authority: {
          decision_maker: true,
          approvers: ['CFO'],
          buying_power: 'Full authority up to $100K'
        },
        need: {
          problem: 'Losing 60% of inbound leads',
          pain_level: 9,
          business_impact: 'Missing $200K/year in revenue'
        },
        timeline: {
          urgency: 'High',
          deadline: '30 days',
          reason: 'Q4 revenue goals at risk'
        },

        // MEDDIC signals
        metrics: {
          target: 'Increase conversion from 30% to 65%',
          revenue_impact: '$200K annually'
        },
        champion: {
          name: 'Sarah Johnson',
          title: 'Head of Marketing',
          influence_level: 'High',
          commitment: 'Actively pushing for this solution'
        },
        decision_criteria: [
          'ROI > 5:1 within 6 months',
          'Easy integration with existing CRM',
          'TCPA compliance built-in'
        ],

        // Intent signals
        intent_signals: {
          gmb_directions: true,
          website_visits: 5,
          email_opens: 3,
          search_query: 'best lead scoring software',
          time_on_site: '12 minutes'
        },

        // Competition
        competitors_evaluating: ['HubSpot', 'Salesforce', 'Internal build'],

        // Psychographics
        psychographic: {
          vals_segment: 'Achiever',
          personality: 'Data-driven, results-focused',
          values: ['Efficiency', 'ROI', 'Innovation']
        }
      }
    })
  });

  const validationResult = await validation.json();
  console.log('Validation Result:');
  console.log('- Total Score:', validationResult.total_score, '/ 150');
  console.log('- Tier:', validationResult.validation_result);
  console.log('- Readiness:', validationResult.readiness_score, '/ 100');
  console.log('- Pass to SDR:', validationResult.pass_to_sdr);
  console.log('- Estimated Close Probability:', validationResult.estimated_close_probability);
  console.log('- Gaps:', validationResult.critical_gaps);
  console.log('- Strengths:', validationResult.strengths);
  console.log('\n');

  // STEP 2: GENERATE SDR OUTREACH (If qualified)
  if (validationResult.pass_to_sdr) {
    console.log('STEP 2: Generating world-class SDR outreach...\n');

    const sdrOutreach = await fetch(API_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        action: 'generate-sdr-outreach',
        contactId, // Same ID - agents share memory!
        businessId,
        useMemory: true,
        data: {
          validation_result: validationResult,
          lead_data: {
            name: 'John Smith',
            company: 'TechCorp',
            title: 'VP of Sales',
            pain: 'Losing $200K/year in revenue from poor lead conversion',
            awareness_level: 'PRODUCT AWARE' // Knows about us
          }
        }
      })
    });

    const sdrResult = await sdrOutreach.json();
    console.log('SDR Strategy:');
    console.log('- Primary Framework:', sdrResult.sdr_strategy.primary_framework);
    console.log('- Channel Sequence:', sdrResult.sdr_strategy.channel_sequence);
    console.log('- Est. Touches to Meeting:', sdrResult.sdr_strategy.estimated_touches_to_meeting);
    console.log('\nEmail Variant A:');
    console.log('Subject:', sdrResult.email_variant_a.subject_line);
    console.log('Body:', sdrResult.email_variant_a.body.substring(0, 200) + '...');
    console.log('CTA:', sdrResult.email_variant_a.cta);
    console.log('\n');

    // STEP 3: LEAD REPLIES (Two-Way Conversation)
    console.log('STEP 3: Lead replies with objection...\n');

    const leadReply = "Thanks for reaching out. I'm interested but $50K seems steep. We're comparing you to HubSpot which is $30K. Can you justify the price difference?";

    const conversation = await fetch(API_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        action: 'handle-conversation',
        contactId, // Same ID - remembers validation + SDR context!
        businessId,
        useMemory: true,
        data: {
          lead_message: leadReply,
          validation_result: validationResult,
          sdr_context: sdrResult
        }
      })
    });

    const conversationResult = await conversation.json();
    console.log('Conversation Analysis:');
    console.log('- Intent Detected:', conversationResult.conversation_analysis.intent);
    console.log('- Sentiment:', conversationResult.conversation_analysis.sentiment);
    console.log('- Objection:', conversationResult.conversation_analysis.objection_detected);
    console.log('- Escalate to Human:', conversationResult.conversation_analysis.escalate_to_human);
    console.log('\nAgent Response:');
    console.log(conversationResult.response.message);
    console.log('\nFramework Used:', conversationResult.response.framework_used);
    console.log('\n');
  }
}

// ==================================================
// EXAMPLE 2: WARM LEAD NURTURE SEQUENCE
// ==================================================

async function example2_WarmLeadNurture() {
  console.log('\n=== EXAMPLE 2: Warm Lead Nurture Sequence ===\n');

  const contactId = 'lead-warm-002';
  const businessId = 'gym-brooklyn-01';

  // STEP 1: VALIDATE (Missing budget + timeline)
  const validation = await fetch(API_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      action: 'validate-lead',
      contactId,
      businessId,
      useMemory: true,
      data: {
        name: 'Sarah Lee',
        email: 'sarah@startup.com',
        title: 'Marketing Manager',

        // BANT gaps
        budget: { allocated: false, note: 'Needs CFO approval' },
        authority: { decision_maker: false, reports_to: 'VP Marketing' },
        need: { problem: 'Lead conversion issues', pain_level: 6 },
        timeline: { urgency: 'Low', note: 'Researching options' },

        // Medium intent
        intent_signals: {
          website_visits: 2,
          email_opens: 1,
          search_query: 'lead scoring tools comparison'
        }
      }
    })
  });

  const validationResult = await validation.json();
  console.log('Validation: TIER 2 WARM (Score:', validationResult.total_score, '/ 150)');
  console.log('Recommendation:', validationResult.recommended_next_action);
  console.log('\n');

  // STEP 2: NURTURE STRATEGY (Educational, not salesy)
  const sdrOutreach = await fetch(API_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      action: 'generate-sdr-outreach',
      contactId,
      businessId,
      useMemory: true,
      data: {
        validation_result: validationResult,
        lead_data: {
          name: 'Sarah Lee',
          company: 'Startup Inc',
          title: 'Marketing Manager',
          awareness_level: 'SOLUTION AWARE' // Knows solutions exist, doesn't know us
        }
      }
    })
  });

  const sdrResult = await sdrOutreach.json();
  console.log('Nurture Strategy:', sdrResult.sdr_strategy.messaging_tone);
  console.log('Email Subject:', sdrResult.email_variant_a.subject_line);
  console.log('Goal: Educate + build trust, NOT hard sell');
  console.log('\n');
}

// ==================================================
// EXAMPLE 3: CHURN RISK DETECTION & RETENTION
// ==================================================

async function example3_ChurnPrevention() {
  console.log('\n=== EXAMPLE 3: Churn Risk Detection & Retention ===\n');

  const contactId = 'customer-churn-001';
  const businessId = 'gym-brooklyn-01';

  // STEP 1: DETECT CHURN RISK
  const churnAnalysis = await fetch(API_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      action: 'analyze-churn-risk',
      contactId,
      businessId,
      useMemory: true,
      data: {
        customer_data: {
          name: 'Mike Johnson',
          email: 'mike@company.com',
          join_date: '2024-03-15',
          plan: 'Pro ($150/month)',
          ltv_to_date: '$1,350',
          tenure_days: 90
        },
        behavioral_data: {
          // CRITICAL SIGNALS
          last_login: '2024-10-15', // 28 days ago
          usage_trend: 'Declining 60%', // Was active, now not
          email_engagement: {
            last_7_emails_opened: 0,
            last_7_emails_sent: 7
          },
          sessions_attended: {
            last_30_days: 2,
            previous_30_days: 15, // Huge drop
            baseline_avg: 12
          },
          support_tickets: [
            {
              date: '2024-10-20',
              issue: 'Too expensive for what I use',
              sentiment: 'NEGATIVE',
              resolved: false
            }
          ],

          // LIFECYCLE SIGNALS
          lifecycle_stage: 'Day 90 (Early plateau - high risk window)',
          renewal_date: '2024-12-15', // 45 days away

          // SENTIMENT SIGNALS
          nps_score: 4, // Detractor
          recent_comments: 'Not seeing results I hoped for'
        }
      }
    })
  });

  const churnResult = await churnAnalysis.json();
  console.log('CHURN RISK ANALYSIS:');
  console.log('- Risk Score:', churnResult.churn_risk_analysis.total_risk_score, '/ 100');
  console.log('- Risk Tier:', churnResult.churn_risk_analysis.risk_tier);
  console.log('- Churn Probability:', churnResult.churn_risk_analysis.estimated_churn_probability);
  console.log('- Days Until Churn:', churnResult.churn_risk_analysis.estimated_days_until_churn);
  console.log('\nTop Risk Factors:');
  churnResult.churn_risk_analysis.top_risk_factors.forEach(factor => {
    console.log('  -', factor);
  });
  console.log('\nRECOMMENDED INTERVENTION:');
  console.log('- Priority:', churnResult.recommended_intervention.priority);
  console.log('- Strategy:', churnResult.recommended_intervention.strategy);
  console.log('- Who Reaches Out:', churnResult.recommended_intervention.who_should_reach_out);
  console.log('- Timeline:', churnResult.recommended_intervention.timeline);
  console.log('\nIntervention Script:');
  console.log(churnResult.intervention_script.opening);
  console.log('\n');
}

// ==================================================
// EXAMPLE 4: FULL CONVERSATION FLOW (Multi-Turn)
// ==================================================

async function example4_MultiTurnConversation() {
  console.log('\n=== EXAMPLE 4: Multi-Turn Conversation (Objection → Resolution) ===\n');

  const contactId = 'lead-conversation-001';
  const businessId = 'gym-brooklyn-01';

  // Turn 1: Lead replies to initial outreach
  console.log('TURN 1: Lead raises price objection\n');
  const turn1 = await fetch(API_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      action: 'handle-conversation',
      contactId,
      businessId,
      useMemory: true,
      data: {
        lead_message: "Interesting, but I think it's too expensive for us right now."
      }
    })
  });

  const turn1Result = await turn1.json();
  console.log('Agent Response:', turn1Result.response.message);
  console.log('Framework:', turn1Result.response.framework_used);
  console.log('\n');

  // Turn 2: Lead provides more context
  console.log('TURN 2: Lead shares real concern\n');
  const turn2 = await fetch(API_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      action: 'handle-conversation',
      contactId, // Same ID - agent remembers Turn 1!
      businessId,
      useMemory: true,
      data: {
        lead_message: "Well, we're a small team and $50K is a big chunk of our budget. We'd need to see really clear ROI."
      }
    })
  });

  const turn2Result = await turn2.json();
  console.log('Agent Response:', turn2Result.response.message);
  console.log('Framework:', turn2Result.response.framework_used);
  console.log('\n');

  // Turn 3: Lead asks for case study
  console.log('TURN 3: Lead asks for proof\n');
  const turn3 = await fetch(API_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      action: 'handle-conversation',
      contactId, // Agent remembers entire conversation!
      businessId,
      useMemory: true,
      data: {
        lead_message: "OK that sounds good. Do you have a case study from a company our size?"
      }
    })
  });

  const turn3Result = await turn3.json();
  console.log('Agent Response:', turn3Result.response.message);
  console.log('Intent Detected:', turn3Result.conversation_analysis.intent);
  console.log('Engagement Level:', turn3Result.conversation_analysis.engagement_level);
  console.log('\n');
}

// ==================================================
// EXAMPLE 5: GROWTH OPPORTUNITY (Upsell)
// ==================================================

async function example5_GrowthOpportunity() {
  console.log('\n=== EXAMPLE 5: Growth Opportunity Detection (Upsell) ===\n');

  const contactId = 'customer-growth-001';
  const businessId = 'gym-brooklyn-01';

  const churnAnalysis = await fetch(API_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      action: 'analyze-churn-risk',
      contactId,
      businessId,
      useMemory: true,
      data: {
        customer_data: {
          name: 'Emily Chen',
          plan: 'Starter ($50/month)',
          tenure_days: 180,
          ltv_to_date: '$900'
        },
        behavioral_data: {
          // CHAMPION SIGNALS (Low churn risk)
          last_login: '2024-11-11', // Yesterday
          usage_trend: 'Increasing 40%',
          sessions_attended: {
            last_30_days: 25,
            hitting_plan_limit: true // KEY UPSELL SIGNAL
          },
          nps_score: 10, // Promoter
          recent_comments: 'Love this! Wish I could do more sessions.',

          // UPSELL SIGNALS
          hitting_limits: ['session_count', 'advanced_features_requested'],
          asked_about_features: ['Pro analytics', 'Team access'],
          growing_company: true // Just got funding
        }
      }
    })
  });

  const growthResult = await churnAnalysis.json();
  console.log('CHURN RISK:', growthResult.churn_risk_analysis.risk_tier, '(CHAMPION)');
  console.log('\nGROWTH OPPORTUNITIES:');
  growthResult.growth_opportunities.forEach(opp => {
    console.log('- Type:', opp.type);
    console.log('  Opportunity:', opp.opportunity);
    console.log('  Action:', opp.recommended_action);
    console.log('  Expansion Revenue:', opp.estimated_expansion_revenue);
    console.log('  Probability:', opp.probability);
  });
  console.log('\n');
}

// ==================================================
// RUN ALL EXAMPLES
// ==================================================

async function runAllExamples() {
  try {
    await example1_HighIntentGMBLead();
    await example2_WarmLeadNurture();
    await example3_ChurnPrevention();
    await example4_MultiTurnConversation();
    await example5_GrowthOpportunity();

    console.log('✅ All examples completed successfully!\n');
    console.log('KEY TAKEAWAYS:');
    console.log('1. Lead Validation uses 12 frameworks (SPIN, MEDDIC, BANT, CHAMP, GPCT, ANUM, FAINT, NEAT, SCOTSMAN, PACT, NOTE, Sandler)');
    console.log('2. SDR Agent uses Eugene Schwartz + Brunson + StoryBrand + Hormozi frameworks');
    console.log('3. Conversation Agent handles objections with human-level judgment');
    console.log('4. Retention Agent prevents churn and identifies growth opportunities');
    console.log('5. All agents share memory - they collaborate seamlessly');
    console.log('6. All use Sonnet 4.5 for world-class quality');
    console.log('\n');
  } catch (error) {
    console.error('Error running examples:', error);
  }
}

// Uncomment to run:
// runAllExamples();

export {
  example1_HighIntentGMBLead,
  example2_WarmLeadNurture,
  example3_ChurnPrevention,
  example4_MultiTurnConversation,
  example5_GrowthOpportunity,
  runAllExamples
};

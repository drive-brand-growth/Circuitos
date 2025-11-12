/**
 * Circuit OS - ML Workflow Optimizer Examples
 *
 * Examples showing how to use the ML-powered workflow optimizer
 * to analyze performance, identify winning patterns, and optimize workflows
 */

const API_URL = 'https://your-vercel-url.vercel.app/api/claude-agent-memory';

// ============================================================================
// EXAMPLE 1: Optimize Underperforming Workflow
// ============================================================================

async function example1_OptimizeUnderperforming() {
  const response = await fetch(API_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      action: 'optimize-workflow',
      contactId: 'optimizer-001',
      businessId: 'my-business-123',
      useMemory: true,
      data: {
        workflowId: 'gmb-workflow-v1',
        performanceData: {
          conversion_rate: 0.35, // 35% (goal: 65%)
          engagement_rate: 0.42, // Email opens/clicks
          roi: 2.1, // Return on investment
          avg_time_to_convert: 8, // Days
          total_leads: 1250,
          total_conversions: 438,
          total_revenue: 65700,
          total_cost: 31200,
          bottlenecks: [
            'Generic messaging (not personalized)',
            'Slow follow-up (24hr delay)',
            'Single-channel (email only)',
            'No SMS consent gate'
          ]
        },
        demographicData: {
          high_converting: {
            age_range: '25-45',
            income_range: '$60K-$120K',
            distance: '<2 miles',
            conversion_rate: 0.78,
            sample_size: 320
          },
          low_converting: {
            age_range: '55+',
            income_range: '<$40K',
            distance: '>5 miles',
            conversion_rate: 0.18,
            sample_size: 180
          }
        },
        psychographicData: {
          health_conscious: {
            values: ['wellness', 'fitness', 'longevity'],
            interests: ['nutrition', 'yoga', 'running'],
            conversion_rate: 0.72,
            avg_ltv: 850,
            sample_size: 280
          },
          price_sensitive: {
            values: ['savings', 'value'],
            interests: ['coupons', 'deals'],
            conversion_rate: 0.28,
            avg_ltv: 320,
            sample_size: 150
          },
          busy_professionals: {
            values: ['convenience', 'efficiency'],
            interests: ['productivity', 'time-management'],
            conversion_rate: 0.64,
            avg_ltv: 920,
            sample_size: 220
          }
        },
        marketTrends: {
          seasonal: {
            name: 'New Year Resolution Season',
            impact: 'Fitness interest peaks in January (+120% vs baseline)',
            recommendation: 'Emphasize transformation stories, before/after'
          },
          industry: {
            name: 'Hybrid Training Growth',
            impact: 'In-person + virtual hybrid models gaining 40% YoY',
            recommendation: 'Offer flexible training options'
          },
          technology: {
            name: 'SMS Engagement Surge',
            impact: 'SMS open rates 98% vs email 22%',
            recommendation: 'Add SMS to high-intent leads'
          }
        }
      }
    })
  });

  const result = await response.json();

  console.log('=== ML OPTIMIZATION RESULTS ===');
  console.log(JSON.stringify(result.optimization, null, 2));

  console.log('\n=== ML SCORE ===');
  console.log(result.optimization.ml_score);

  console.log('\n=== OPTIMIZATIONS (PRIORITIZED) ===');
  result.optimization.optimizations.forEach(opt => {
    console.log(`${opt.priority}. ${opt.type} - Expected lift: ${opt.expected_lift}`);
  });

  console.log('\n=== A/B TESTS ===');
  result.optimization.ab_tests.forEach(test => {
    console.log(`${test.test_id}: ${test.hypothesis}`);
  });
}

// ============================================================================
// EXAMPLE 2: Analyze Demographic Patterns
// ============================================================================

async function example2_DemographicAnalysis() {
  const response = await fetch(API_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      action: 'optimize-workflow',
      contactId: 'optimizer-002',
      businessId: 'my-business-123',
      useMemory: true,
      data: {
        workflowId: 'email-nurture-v2',
        performanceData: {
          conversion_rate: 0.52,
          total_leads: 800
        },
        demographicData: {
          millennials: {
            age_range: '25-40',
            conversion_rate: 0.68,
            preferred_channel: 'SMS',
            avg_ltv: 920,
            sample_size: 350
          },
          gen_x: {
            age_range: '41-56',
            conversion_rate: 0.58,
            preferred_channel: 'Email',
            avg_ltv: 1150,
            sample_size: 280
          },
          boomers: {
            age_range: '57+',
            conversion_rate: 0.32,
            preferred_channel: 'Phone',
            avg_ltv: 680,
            sample_size: 170
          }
        }
      }
    })
  });

  const result = await response.json();

  console.log('=== DEMOGRAPHIC INSIGHTS ===');
  console.log(result.optimization.winning_patterns.demographics);

  // ML will recommend:
  // 1. Segment by age (create 3 separate workflows)
  // 2. Use preferred channels (SMS for Millennials, Email for Gen X, Phone for Boomers)
  // 3. Customize messaging per generation
}

// ============================================================================
// EXAMPLE 3: Psychographic Optimization
// ============================================================================

async function example3_PsychographicOptimization() {
  const response = await fetch(API_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      action: 'optimize-workflow',
      contactId: 'optimizer-003',
      businessId: 'my-business-123',
      useMemory: true,
      data: {
        workflowId: 'gmb-high-intent-v1',
        performanceData: {
          conversion_rate: 0.45,
          total_leads: 600
        },
        psychographicData: {
          achievers: {
            profile: {
              values: ['success', 'status', 'achievement'],
              personality: 'competitive, goal-oriented',
              messaging_style: 'challenge-based, results-focused'
            },
            conversion_rate: 0.82,
            avg_ltv: 1250,
            sample_size: 180
          },
          nurturers: {
            profile: {
              values: ['family', 'community', 'relationships'],
              personality: 'empathetic, supportive',
              messaging_style: 'community-focused, inclusive'
            },
            conversion_rate: 0.64,
            avg_ltv: 890,
            sample_size: 150
          },
          budget_conscious: {
            profile: {
              values: ['value', 'savings', 'practicality'],
              personality: 'analytical, cautious',
              messaging_style: 'ROI-focused, transparent pricing'
            },
            conversion_rate: 0.28,
            avg_ltv: 420,
            sample_size: 270
          }
        }
      }
    })
  });

  const result = await response.json();

  console.log('=== PSYCHOGRAPHIC OPTIMIZATION ===');
  console.log(result.optimization.optimizations);

  // ML will recommend:
  // 1. Segment by psychographic profile
  // 2. Customize copy per persona:
  //    - Achievers: "Beat your personal best", "Join the top 1%"
  //    - Nurturers: "Join our community", "Bring a friend"
  //    - Budget-Conscious: "$49/mo = $1.60/day", "No hidden fees"
}

// ============================================================================
// EXAMPLE 4: Trigger Analysis & Optimization
// ============================================================================

async function example4_TriggerOptimization() {
  const response = await fetch(API_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      action: 'optimize-workflow',
      contactId: 'optimizer-004',
      businessId: 'my-business-123',
      useMemory: true,
      data: {
        workflowId: 'multi-trigger-v1',
        performanceData: {
          conversion_rate: 0.48,
          total_leads: 1500
        },
        demographicData: {}, // Minimal demo data
        psychographicData: {},
        marketTrends: {},
        triggerAnalysis: {
          gmb_directions: {
            conversion_rate: 0.85,
            roi: 5.2,
            sample_size: 320,
            avg_time_to_convert: 2, // days
            recommended_action: 'Immediate SMS (within 5 min)'
          },
          gmb_call: {
            conversion_rate: 0.92,
            roi: 6.8,
            sample_size: 180,
            avg_time_to_convert: 1,
            recommended_action: 'Call back within 15 min'
          },
          website_visit: {
            conversion_rate: 0.43,
            roi: 2.1,
            sample_size: 650,
            avg_time_to_convert: 7,
            recommended_action: 'Email nurture sequence'
          },
          form_fill: {
            conversion_rate: 0.62,
            roi: 3.4,
            sample_size: 280,
            avg_time_to_convert: 4,
            recommended_action: 'Email + SMS combo'
          },
          social_engagement: {
            conversion_rate: 0.18,
            roi: 0.9,
            sample_size: 420,
            avg_time_to_convert: 14,
            recommended_action: 'Low-touch nurture'
          }
        }
      }
    })
  });

  const result = await response.json();

  console.log('=== TRIGGER OPTIMIZATION ===');
  console.log(result.optimization.winning_patterns.triggers);

  // ML will recommend:
  // 1. Prioritize by conversion rate: GMB call > GMB directions > Form fill > Website > Social
  // 2. Speed to lead: High-intent (GMB) = <15 min, Medium = <2 hrs, Low = 24 hrs
  // 3. Channel matching: GMB = SMS, Website = Email, Social = Retargeting ads
}

// ============================================================================
// EXAMPLE 5: Market Trend Adaptation
// ============================================================================

async function example5_MarketTrendAdaptation() {
  const response = await fetch(API_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      action: 'optimize-workflow',
      contactId: 'optimizer-005',
      businessId: 'my-business-123',
      useMemory: true,
      data: {
        workflowId: 'seasonal-campaign-v1',
        performanceData: {
          conversion_rate: 0.38
        },
        marketTrends: {
          seasonal: [
            {
              month: 'January',
              trend: 'New Year resolutions',
              impact: '+120% fitness interest',
              messaging: 'Emphasize transformation, fresh start'
            },
            {
              month: 'February',
              trend: 'Valentine\'s Day',
              impact: '+40% couples/partner activities',
              messaging: 'Partner workouts, bring-a-friend deals'
            },
            {
              month: 'Summer (June-Aug)',
              trend: 'Beach season',
              impact: '+80% weight loss focus',
              messaging: 'Summer body goals, outdoor training'
            },
            {
              month: 'September',
              trend: 'Back-to-school',
              impact: '+60% schedule-focused',
              messaging: 'Flexible hours, family plans'
            }
          ],
          economic: {
            status: 'Recession concerns',
            impact: 'Price sensitivity up 35%',
            recommendation: 'Emphasize ROI, payment plans, value-stacking'
          },
          competitive: {
            trend: '$1 trial offers increasing',
            impact: 'Higher entry barrier with $49 first session',
            recommendation: 'Match or offer alternative (free consultation)'
          }
        }
      }
    })
  });

  const result = await response.json();

  console.log('=== MARKET TREND INSIGHTS ===');
  console.log(result.optimization.winning_patterns.market_trends);

  // ML will recommend:
  // 1. Create seasonal workflow variants
  // 2. Adjust messaging per season (January = transformation, Summer = beach body)
  // 3. Address economic concerns (emphasize value, payment plans)
  // 4. Competitive response (trial offer or alternative incentive)
}

// ============================================================================
// EXAMPLE 6: A/B Test Design from ML Insights
// ============================================================================

async function example6_ABTestDesign() {
  const response = await fetch(API_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      action: 'optimize-workflow',
      contactId: 'optimizer-006',
      businessId: 'my-business-123',
      useMemory: true,
      data: {
        workflowId: 'email-campaign-v3',
        performanceData: {
          conversion_rate: 0.42,
          open_rate: 0.28,
          click_rate: 0.12
        },
        // ML will analyze and suggest A/B tests
      }
    })
  });

  const result = await response.json();

  console.log('=== RECOMMENDED A/B TESTS ===');
  result.optimization.ab_tests.forEach(test => {
    console.log(`\nTest: ${test.test_id}`);
    console.log(`Hypothesis: ${test.hypothesis}`);
    console.log(`Variant A: ${test.variant_a.description}`);
    console.log(`Variant B: ${test.variant_b.description}`);
    console.log(`Expected winner: ${test.expected_winner}`);
    console.log(`Sample size needed: ${test.sample_size}`);
  });

  // ML might suggest:
  // - Test 1: Curiosity vs Benefit-driven subject lines
  // - Test 2: Psychographic copy vs Generic copy
  // - Test 3: Email-only vs Email+SMS combo
  // - Test 4: Immediate send vs Timing optimization
}

// ============================================================================
// EXAMPLE 7: Continuous Improvement Loop
// ============================================================================

async function example7_ContinuousImprovement() {
  // Week 1: Initial optimization
  const optimization1 = await fetch(API_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      action: 'optimize-workflow',
      contactId: 'optimizer-007-continuous', // SAME ID for memory
      businessId: 'my-business-123',
      useMemory: true,
      data: {
        workflowId: 'gmb-workflow-v1',
        performanceData: { conversion_rate: 0.35 }
      }
    })
  });

  const result1 = await optimization1.json();
  console.log('=== WEEK 1 OPTIMIZATION ===');
  console.log(`Projected conversion: ${result1.optimization.projected_performance.conversion_rate}`);

  // Week 3: Re-optimize with new data (ML remembers previous optimization!)
  const optimization2 = await fetch(API_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      action: 'optimize-workflow',
      contactId: 'optimizer-007-continuous', // SAME ID
      businessId: 'my-business-123',
      useMemory: true,
      data: {
        workflowId: 'gmb-workflow-v2', // Implemented changes
        performanceData: {
          conversion_rate: 0.58, // Improved from 0.35!
          note: 'Implemented segmentation + SMS'
        }
      }
    })
  });

  const result2 = await optimization2.json();
  console.log('\n=== WEEK 3 RE-OPTIMIZATION ===');
  console.log('ML sees previous optimization and new results...');
  console.log(`Actual lift: ${((0.58 - 0.35) / 0.35 * 100).toFixed(1)}%`);
  console.log('Next optimizations:', result2.optimization.optimizations);

  // ML learns: "Segmentation worked well, let's test psychographic personalization next"
}

// ============================================================================
// RUNNING THE EXAMPLES
// ============================================================================

async function runAllExamples() {
  console.log('========================================');
  console.log('ML WORKFLOW OPTIMIZER EXAMPLES');
  console.log('========================================\n');

  await example1_OptimizeUnderperforming();
  console.log('\n\n');

  await example2_DemographicAnalysis();
  console.log('\n\n');

  await example3_PsychographicOptimization();
  console.log('\n\n');

  await example4_TriggerOptimization();
  console.log('\n\n');

  await example5_MarketTrendAdaptation();
  console.log('\n\n');

  await example6_ABTestDesign();
  console.log('\n\n');

  await example7_ContinuousImprovement();
}

// Uncomment to run:
// runAllExamples();

export {
  example1_OptimizeUnderperforming,
  example2_DemographicAnalysis,
  example3_PsychographicOptimization,
  example4_TriggerOptimization,
  example5_MarketTrendAdaptation,
  example6_ABTestDesign,
  example7_ContinuousImprovement
};

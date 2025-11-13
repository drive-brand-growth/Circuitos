/**
 * Lead Routing Agent - Intelligent Rep Assignment (Enhanced with Geo-Intelligence)
 *
 * Assigns leads to optimal sales reps based on:
 * - Rep availability & capacity
 * - Rep specialization (industry, product expertise)
 * - Geographic territory (ENHANCED: drive time, territory coverage)
 * - Historical performance (close rate with similar leads)
 * - Current workload balance
 *
 * NEW (v2.0 with Google Maps AI):
 * - Actual drive time calculations (not just distance)
 * - Territory density analysis
 * - Route optimization for multi-lead days
 * - Market coverage scoring
 *
 * Uses ML + round-robin + performance-based routing + geo-intelligence
 */

import Anthropic from '@anthropic-ai/sdk';
import { calculateDriveTime } from './geo-lpr-agent.js';
import { enrichLead } from './lead-enrichment-service.js';

const anthropic = new Anthropic({
  apiKey: process.env.CLAUDE_API_KEY
});

const LEAD_ROUTING_AGENT_PROMPT = `You are the **Lead Routing Agent**, responsible for intelligently assigning leads to the optimal sales rep.

## YOUR ROLE

Given a lead and available sales reps, you determine:
1. **Best Rep Match** - Which rep is most likely to close this lead?
2. **Routing Logic** - Round-robin vs performance-based vs specialized
3. **Capacity Check** - Does rep have bandwidth?
4. **Backup Assignment** - If primary rep unavailable, who's next?

---

## ROUTING CRITERIA (Priority Order)

### 1. AVAILABILITY (Must-Have)
- Rep status: AVAILABLE, BUSY, OUT_OF_OFFICE, ON_CALL
- Current lead capacity: Active leads vs max capacity
- Response time: Average time to first contact

**Rules:**
- If rep has ≥ max_capacity leads → SKIP
- If rep status = OUT_OF_OFFICE → SKIP
- If rep hasn't responded to last 3 leads → DEPRIORITIZE

### 2. SPECIALIZATION (High Priority)
- **Industry Expertise**: Gym specialist vs Med Spa specialist vs Home Services
- **Product Expertise**: Technical sale vs simple sale
- **Lead Tier**: Enterprise rep vs SMB rep
- **Language**: Bilingual reps for non-English leads

**Scoring:**
- Perfect match (gym rep + gym lead): +50 points
- Partial match (fitness industry experience): +25 points
- No match (generic): 0 points

### 3. TERRITORY (High Priority)
- **Geographic Coverage**: US regions, states, cities
- **Time Zone**: Rep in same TZ as lead (faster response)
- **Local Knowledge**: Rep familiar with local market

**Scoring:**
- Same city: +30 points
- Same state: +20 points
- Same region: +10 points
- Different time zone: -10 points

### 4. HISTORICAL PERFORMANCE (Medium Priority)
- **Close Rate with Similar Leads**: Has this rep closed leads like this before?
- **Average Deal Size**: Does rep handle deals of this size?
- **Sales Cycle Length**: How fast does rep close?

**Scoring:**
- Close rate > 50% with similar leads: +40 points
- Close rate 30-50%: +20 points
- Close rate < 30%: 0 points
- Never closed this lead type: -10 points

### 5. WORKLOAD BALANCE (Low Priority)
- **Active Leads**: How many leads does rep currently have?
- **Pipeline Value**: Total $ value of rep's pipeline
- **Last Assignment**: When was rep last assigned a lead?

**Scoring:**
- Below avg workload: +15 points
- Average workload: 0 points
- Above avg workload: -15 points

---

## ROUTING STRATEGIES

### **Strategy 1: Performance-Based (Default for Hot Leads)**
Route TIER 1 HOT leads (score 130-150) to **TOP PERFORMERS**

\`\`\`
Prioritize:
1. Highest close rate with similar leads
2. Specialization match
3. Available capacity

Logic:
- Hot leads are valuable → give to best closers
- Ignore workload balance (top performers get more leads)
\`\`\`

### **Strategy 2: Round-Robin (Fair Distribution)**
Route TIER 2 WARM leads (score 90-129) evenly across team

\`\`\`
Prioritize:
1. Longest time since last assignment
2. Below average workload
3. Specialization match (if applicable)

Logic:
- Warm leads need nurturing → distribute fairly
- Build skills across team
\`\`\`

### **Strategy 3: Specialized Routing (Complex Sales)**
Route complex/enterprise leads to **SPECIALISTS**

\`\`\`
Prioritize:
1. Specialization match (must-have)
2. Experience with deal size
3. Technical expertise

Logic:
- Complex sales require specific skills
- Mismatch = lost deal
\`\`\`

---

## ASSIGNMENT LOGIC

\`\`\`
FOR EACH LEAD:

1. Classify lead tier (HOT/WARM/COLD)
2. Identify required specialization (if any)
3. Filter available reps:
   - Status = AVAILABLE or ON_CALL
   - Capacity < max_capacity
   - Specialization match (if required)

4. Score each available rep:
   - Specialization: 0-50 points
   - Territory: 0-30 points
   - Performance: 0-40 points
   - Workload: -15 to +15 points
   - TOTAL: 0-135 points

5. Select top-scoring rep
6. Assign + notify rep
7. Log assignment for ML learning

IF NO REP AVAILABLE:
- Queue lead for next available rep
- Notify sales manager
- Set auto-follow-up reminder
\`\`\`

---

## OUTPUT FORMAT (STRICT JSON)

\`\`\`json
{
  "routing_decision": {
    "assigned_rep": {
      "rep_id": "rep-001",
      "name": "Sarah Johnson",
      "email": "sarah@company.com",
      "phone": "+1-555-0100"
    },
    "routing_strategy": "PERFORMANCE_BASED",
    "assignment_priority": "HIGH (TIER 1 HOT lead)",
    "expected_response_time": "< 5 minutes",
    "estimated_close_probability": "75%"
  },

  "scoring_breakdown": {
    "rep_001_sarah_johnson": {
      "total_score": 115,
      "breakdown": {
        "specialization": 50,
        "reason": "Perfect match - gym specialist + gym lead"
      },
      {
        "territory": 30,
        "reason": "Same city (Brooklyn, NY)"
      },
      {
        "performance": 40,
        "reason": "65% close rate with similar leads (gym owners, $50K deals)"
      },
      {
        "workload": -5,
        "reason": "Slightly above avg workload (12 active leads vs 10 avg)"
      }
    },
    "rep_002_mike_chen": {
      "total_score": 85,
      "breakdown": {
        "specialization": 25,
        "reason": "Partial match - fitness industry experience"
      },
      {
        "territory": 20,
        "reason": "Same state (NY) but different city"
      },
      {
        "performance": 30,
        "reason": "45% close rate with similar leads"
      },
      {
        "workload": 10,
        "reason": "Below avg workload (7 active leads)"
      }
    }
  },

  "assignment_details": {
    "lead_id": "lead-001",
    "lead_name": "John Smith",
    "lead_tier": "TIER 1: HOT",
    "lead_score": 142,
    "lead_industry": "Fitness (gym owner)",
    "lead_location": "Brooklyn, NY",
    "lead_deal_size": "$50,000",
    "assigned_to": "Sarah Johnson (rep-001)",
    "assigned_at": "2025-11-12T14:30:00Z",
    "notification_sent": true,
    "backup_rep": "Mike Chen (rep-002)"
  },

  "rep_capacity_status": {
    "rep_001_sarah_johnson": {
      "status": "AVAILABLE",
      "active_leads": 12,
      "max_capacity": 15,
      "utilization": "80%",
      "avg_response_time": "3 minutes"
    },
    "rep_002_mike_chen": {
      "status": "AVAILABLE",
      "active_leads": 7,
      "max_capacity": 15,
      "utilization": "47%",
      "avg_response_time": "8 minutes"
    }
  },

  "ml_insights": {
    "similar_leads_closed_by_sarah": {
      "count": 23,
      "close_rate": "65%",
      "avg_deal_size": "$48,500",
      "avg_sales_cycle": "32 days"
    },
    "recommendation": "Sarah has strong track record with gym owners in NYC. Assign with high confidence.",
    "alternative_if_unavailable": "Mike Chen is backup (45% close rate, but lower workload)"
  },

  "notifications": [
    {
      "recipient": "Sarah Johnson",
      "method": "SMS + Email + CRM notification",
      "message": "New HOT lead assigned: John Smith (gym owner, Brooklyn, score 142/150). Contact within 5 minutes for best results.",
      "priority": "HIGH",
      "include_lead_summary": true
    },
    {
      "recipient": "Sales Manager",
      "method": "Slack notification",
      "message": "HOT lead (John Smith, $50K) assigned to Sarah Johnson. Monitor for response.",
      "priority": "MEDIUM"
    }
  ],

  "follow_up_triggers": [
    {
      "trigger": "If no contact within 10 minutes",
      "action": "Notify sales manager + reassign to backup rep (Mike Chen)"
    },
    {
      "trigger": "If lead doesn't respond within 24 hours",
      "action": "Trigger nurture sequence"
    },
    {
      "trigger": "If lead goes cold after 7 days",
      "action": "Reassign to junior rep for long-term nurture"
    }
  ]
}
\`\`\`

---

## CRITICAL RULES

1. **Speed Matters**: Hot leads assigned within 60 seconds
2. **No Lead Left Behind**: If all reps at capacity, queue + notify manager
3. **Specialization Trumps Workload**: Better to overload specialist than assign to generalist (for complex sales)
4. **Track Everything**: Log assignments for ML learning (which assignments work?)
5. **Backup Always**: Every assignment has backup rep in case primary unavailable
6. **Fair Distribution**: Over time, use round-robin to balance workload

---

Remember: Your job is to maximize close rate by matching the right lead to the right rep at the right time.`;

/**
 * Route lead to optimal sales rep
 */
export async function routeLead(leadData, validationResult, availableReps, historicalData) {
  const userPrompt = `
LEAD DATA:
${JSON.stringify(leadData, null, 2)}

LEAD VALIDATION RESULT:
${JSON.stringify(validationResult, null, 2)}

AVAILABLE SALES REPS:
${JSON.stringify(availableReps, null, 2)}

HISTORICAL PERFORMANCE DATA:
${JSON.stringify(historicalData, null, 2)}

---

**TASK**: Assign this lead to the optimal sales rep.

Requirements:
1. Classify lead tier (HOT/WARM/COLD) from validation score
2. Score each available rep (specialization, territory, performance, workload)
3. Select top-scoring rep
4. Provide backup rep
5. Generate notifications
6. Set follow-up triggers

Return ONLY valid JSON matching the output format.`;

  const message = await anthropic.messages.create({
    model: 'claude-sonnet-4-5-20250929', // Routing decisions are revenue-critical
    max_tokens: 4096,
    temperature: 0.2, // Low temp for consistent, analytical decisions
    system: LEAD_ROUTING_AGENT_PROMPT,
    messages: [{ role: 'user', content: userPrompt }]
  });

  const responseText = message.content[0].text;

  // Extract JSON from response
  let jsonText = responseText;
  if (responseText.includes('```json')) {
    jsonText = responseText.split('```json')[1].split('```')[0].trim();
  } else if (responseText.includes('```')) {
    jsonText = responseText.split('```')[1].split('```')[0].trim();
  }

  const result = JSON.parse(jsonText);

  return {
    ...result,
    token_usage: {
      input: message.usage.input_tokens,
      output: message.usage.output_tokens
    }
  };
}

/**
 * Enhanced Lead Routing with Geo-Intelligence (v2.0)
 *
 * @param {Object} leadData - Lead information
 * @param {Object} validationResult - Lead validation score/tier
 * @param {Array<Object>} availableReps - Sales reps with location data
 * @param {Object} historicalData - Historical performance
 * @param {Object} options
 *   - enable_geo_intelligence: boolean (default true)
 *   - max_drive_time_minutes: number (default 60)
 *   - prioritize_territory: boolean (default false)
 * @returns {Promise<Object>} Enhanced routing decision with drive times
 */
export async function routeLeadWithGeoIntelligence(
  leadData,
  validationResult,
  availableReps,
  historicalData,
  options = {}
) {
  const {
    enable_geo_intelligence = true,
    max_drive_time_minutes = 60,
    prioritize_territory = false
  } = options;

  // Step 1: Enrich lead with location data (if not already enriched)
  let enrichedLead = leadData;
  if (enable_geo_intelligence && !leadData.location) {
    try {
      enrichedLead = await enrichLead(leadData, { include_competitors: false });
    } catch (error) {
      console.log('Could not enrich lead location, using basic routing');
      enrichedLead = leadData;
    }
  }

  // Step 2: Calculate drive times for each rep (if lead has location)
  const repsWithDriveTime = [];

  if (enable_geo_intelligence && enrichedLead.location) {
    for (const rep of availableReps) {
      if (rep.base_location?.lat && rep.base_location?.lng) {
        try {
          const driveTime = await calculateDriveTime(
            rep.base_location,
            enrichedLead.location,
            'driving'
          );

          repsWithDriveTime.push({
            ...rep,
            drive_time: driveTime,
            within_territory: driveTime.duration.minutes <= max_drive_time_minutes,
            territory_score: calculateTerritoryScore(driveTime.duration.minutes, max_drive_time_minutes)
          });
        } catch (error) {
          console.error(`Error calculating drive time for rep ${rep.name}:`, error);
          repsWithDriveTime.push({
            ...rep,
            drive_time: null,
            within_territory: true, // Assume yes if can't calculate
            territory_score: 15 // Average score
          });
        }
      } else {
        // Rep doesn't have location data
        repsWithDriveTime.push({
          ...rep,
          drive_time: null,
          within_territory: true,
          territory_score: 15
        });
      }
    }

    // Filter out reps outside max drive time (if prioritizing territory)
    const filteredReps = prioritize_territory
      ? repsWithDriveTime.filter(r => r.within_territory)
      : repsWithDriveTime;

    // If no reps within territory, expand search
    const repsToUse = filteredReps.length > 0 ? filteredReps : repsWithDriveTime;

    // Step 3: Call standard routing with enhanced territory data
    const routingDecision = await routeLead(
      enrichedLead,
      validationResult,
      repsToUse,
      historicalData
    );

    // Step 4: Enhance response with geo-intelligence insights
    const assignedRep = repsToUse.find(r => r.rep_id === routingDecision.routing_decision.assigned_rep.rep_id);

    return {
      ...routingDecision,
      geo_intelligence: {
        lead_location: enrichedLead.location,
        lead_enrichment_status: enrichedLead.enrichment_status,
        assigned_rep_drive_time: assignedRep?.drive_time,
        territory_fit: assignedRep?.within_territory ? 'GOOD' : 'OUT_OF_TERRITORY',
        territory_score: assignedRep?.territory_score || 0,
        all_reps_drive_times: repsWithDriveTime.map(r => ({
          rep_name: r.name,
          drive_time_minutes: r.drive_time?.duration.minutes,
          distance_miles: r.drive_time?.distance.miles,
          within_territory: r.within_territory
        })),
        routing_recommendation: generateGeoRoutingRecommendation(assignedRep, repsWithDriveTime)
      }
    };

  } else {
    // Geo-intelligence disabled or no location data - use standard routing
    return await routeLead(leadData, validationResult, availableReps, historicalData);
  }
}

/**
 * Calculate territory score based on drive time
 *
 * Closer = better score
 */
function calculateTerritoryScore(driveTimeMinutes, maxDriveTime) {
  if (driveTimeMinutes <= 20) {
    return 30; // Excellent - very close
  } else if (driveTimeMinutes <= 30) {
    return 25; // Good - reasonable distance
  } else if (driveTimeMinutes <= 45) {
    return 20; // Fair - manageable
  } else if (driveTimeMinutes <= maxDriveTime) {
    return 10; // Marginal - edge of territory
  } else {
    return 0; // Out of territory
  }
}

/**
 * Generate geo-specific routing recommendation
 */
function generateGeoRoutingRecommendation(assignedRep, allReps) {
  if (!assignedRep?.drive_time) {
    return 'Standard routing applied (no location data available)';
  }

  const driveTimeMinutes = assignedRep.drive_time.duration.minutes;
  const closerReps = allReps.filter(r =>
    r.drive_time &&
    r.drive_time.duration.minutes < driveTimeMinutes &&
    r.status === 'AVAILABLE'
  );

  if (driveTimeMinutes <= 20) {
    return `Excellent territory fit. Rep is ${driveTimeMinutes} minutes away (${assignedRep.drive_time.distance.miles} miles). Optimal for in-person meetings.`;
  } else if (driveTimeMinutes <= 45) {
    if (closerReps.length > 0) {
      return `Good territory fit (${driveTimeMinutes} mins away), though ${closerReps.length} rep(s) are closer. Assigned based on specialization/performance.`;
    } else {
      return `Good territory fit. Rep is ${driveTimeMinutes} minutes away. Reasonable for in-person meetings.`;
    }
  } else if (driveTimeMinutes <= 60) {
    return `Marginal territory fit (${driveTimeMinutes} mins away). Consider virtual meeting first, in-person if deal size justifies.`;
  } else {
    return `Out of primary territory (${driveTimeMinutes} mins away). Recommend virtual meeting or consider reassignment if in-person required.`;
  }
}

/**
 * Analyze territory coverage for team
 *
 * @param {Array<Object>} salesReps - Reps with base_location
 * @param {Array<Object>} leads - Leads with location data
 * @returns {Object} Territory coverage analysis
 */
export async function analyzeTerritoryCoverage(salesReps, leads) {
  const coverage = {
    total_reps: salesReps.length,
    total_leads: leads.length,
    coverage_by_rep: [],
    uncovered_leads: [],
    territory_gaps: []
  };

  // For each rep, find leads within their territory (60 min drive)
  for (const rep of salesReps) {
    if (!rep.base_location?.lat || !rep.base_location?.lng) {
      coverage.coverage_by_rep.push({
        rep_name: rep.name,
        rep_id: rep.rep_id,
        error: 'No location data'
      });
      continue;
    }

    const leadsInTerritory = [];

    for (const lead of leads) {
      if (lead.location?.lat && lead.location?.lng) {
        try {
          const driveTime = await calculateDriveTime(
            rep.base_location,
            lead.location,
            'driving'
          );

          if (driveTime.duration.minutes <= 60) {
            leadsInTerritory.push({
              lead_name: lead.business_name || lead.name,
              drive_time_minutes: driveTime.duration.minutes,
              distance_miles: driveTime.distance.miles
            });
          }
        } catch (error) {
          // Skip this lead
        }
      }
    }

    coverage.coverage_by_rep.push({
      rep_name: rep.name,
      rep_id: rep.rep_id,
      base_location: `${rep.city}, ${rep.state}`,
      leads_in_territory: leadsInTerritory.length,
      leads: leadsInTerritory,
      territory_density: leadsInTerritory.length >= 20 ? 'HIGH' :
                         leadsInTerritory.length >= 10 ? 'MEDIUM' : 'LOW'
    });
  }

  // Find leads not covered by any rep
  for (const lead of leads) {
    if (!lead.location?.lat || !lead.location?.lng) continue;

    let covered = false;
    for (const repCoverage of coverage.coverage_by_rep) {
      if (repCoverage.leads?.some(l => l.lead_name === (lead.business_name || lead.name))) {
        covered = true;
        break;
      }
    }

    if (!covered) {
      coverage.uncovered_leads.push({
        lead_name: lead.business_name || lead.name,
        location: `${lead.city}, ${lead.state}`,
        reason: 'No rep within 60 minute drive time'
      });
    }
  }

  // Identify territory gaps
  if (coverage.uncovered_leads.length > 0) {
    const gapLocations = {};
    coverage.uncovered_leads.forEach(lead => {
      const locationKey = lead.location;
      gapLocations[locationKey] = (gapLocations[locationKey] || 0) + 1;
    });

    Object.entries(gapLocations).forEach(([location, count]) => {
      if (count >= 3) { // 3+ uncovered leads in same area = gap
        coverage.territory_gaps.push({
          location,
          uncovered_lead_count: count,
          recommendation: count >= 10
            ? `HIGH PRIORITY: ${count} leads in ${location}. Consider hiring rep here.`
            : `MEDIUM PRIORITY: ${count} leads in ${location}. Expand nearby rep's territory or use virtual selling.`
        });
      }
    });
  }

  return {
    ...coverage,
    summary: {
      coverage_rate: ((leads.length - coverage.uncovered_leads.length) / leads.length) * 100,
      avg_leads_per_rep: coverage.coverage_by_rep.reduce((sum, r) => sum + (r.leads_in_territory || 0), 0) / salesReps.length,
      territory_gaps_count: coverage.territory_gaps.length,
      recommendation: generateCoverageRecommendation(coverage)
    },
    analyzed_at: new Date().toISOString()
  };
}

/**
 * Generate territory coverage recommendation
 */
function generateCoverageRecommendation(coverage) {
  const coverageRate = ((coverage.total_leads - coverage.uncovered_leads.length) / coverage.total_leads) * 100;

  if (coverageRate >= 90) {
    return 'Excellent territory coverage. Current team can handle lead volume.';
  } else if (coverageRate >= 75) {
    return `Good coverage (${Math.round(coverageRate)}%), but ${coverage.uncovered_leads.length} leads outside territories. Consider expanding rep territories or hiring.`;
  } else if (coverageRate >= 50) {
    return `Moderate coverage (${Math.round(coverageRate)}%). ${coverage.territory_gaps.length} territory gaps identified. Recommend hiring additional reps in gap areas.`;
  } else {
    return `Poor coverage (${Math.round(coverageRate)}%). Major territory gaps. Urgent: Hire additional reps or transition to virtual-first selling model.`;
  }
}

/**
 * Optimize daily route for rep visiting multiple leads
 *
 * @param {Object} rep - Rep with base_location
 * @param {Array<Object>} leadsToVisit - Leads with location data
 * @returns {Promise<Object>} Optimized route
 */
export async function optimizeDailyRoute(rep, leadsToVisit) {
  if (!rep.base_location || leadsToVisit.length === 0) {
    return {
      error: 'Rep location or leads missing',
      route: []
    };
  }

  // Simple greedy algorithm: nearest neighbor
  const route = [];
  let currentLocation = rep.base_location;
  const remainingLeads = [...leadsToVisit];

  while (remainingLeads.length > 0) {
    let closestLead = null;
    let shortestTime = Infinity;
    let closestIndex = -1;

    for (let i = 0; i < remainingLeads.length; i++) {
      const lead = remainingLeads[i];
      if (!lead.location) continue;

      const driveTime = await calculateDriveTime(currentLocation, lead.location, 'driving');

      if (driveTime.duration.minutes < shortestTime) {
        shortestTime = driveTime.duration.minutes;
        closestLead = lead;
        closestIndex = i;
      }
    }

    if (closestLead) {
      route.push({
        order: route.length + 1,
        lead_name: closestLead.business_name || closestLead.name,
        lead_id: closestLead.lead_id,
        location: closestLead.location,
        drive_time_from_previous: shortestTime,
        estimated_meeting_duration: closestLead.estimated_meeting_duration || 60, // minutes
        arrival_time: null // Calculate below
      });

      currentLocation = closestLead.location;
      remainingLeads.splice(closestIndex, 1);
    } else {
      break; // No more reachable leads
    }
  }

  // Calculate arrival times (assuming 9am start)
  let currentTime = 9 * 60; // 9am in minutes
  route.forEach(stop => {
    currentTime += stop.drive_time_from_previous;
    stop.arrival_time = formatTime(currentTime);
    currentTime += stop.estimated_meeting_duration;
  });

  const totalDriveTime = route.reduce((sum, stop) => sum + stop.drive_time_from_previous, 0);
  const totalMeetingTime = route.reduce((sum, stop) => sum + stop.estimated_meeting_duration, 0);

  return {
    rep_name: rep.name,
    date: new Date().toISOString().split('T')[0],
    total_stops: route.length,
    route: route,
    summary: {
      total_drive_time_minutes: totalDriveTime,
      total_meeting_time_minutes: totalMeetingTime,
      total_time_minutes: totalDriveTime + totalMeetingTime,
      estimated_end_time: formatTime(currentTime),
      feasibility: currentTime <= 17 * 60 ? 'FEASIBLE' : 'TOO_LONG' // 5pm = 17:00
    },
    optimized_at: new Date().toISOString()
  };
}

/**
 * Helper: Format minutes since midnight to HH:MM AM/PM
 */
function formatTime(minutes) {
  const hours = Math.floor(minutes / 60);
  const mins = minutes % 60;
  const period = hours >= 12 ? 'PM' : 'AM';
  const displayHours = hours > 12 ? hours - 12 : hours === 0 ? 12 : hours;

  return `${displayHours}:${mins.toString().padStart(2, '0')} ${period}`;
}

export default {
  routeLead,
  routeLeadWithGeoIntelligence,
  analyzeTerritoryCoverage,
  optimizeDailyRoute
};

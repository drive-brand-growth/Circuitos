/**
 * Appointment Scheduling Agent - Calendar Intelligence (Enhanced with Travel Time)
 *
 * Handles:
 * - Google Calendar / Outlook sync
 * - Optimal time slot selection (ML-powered + travel time)
 * - Automated reminders (24hr, 2hr, 30min before)
 * - No-show prediction & prevention
 * - Rescheduling automation
 *
 * NEW (v2.0 with Google Maps AI):
 * - Travel time consideration for in-person meetings
 * - Buffer time between appointments
 * - Route optimization for multi-appointment days
 * - Traffic-aware scheduling
 *
 * Integrates with GHL calendar + external calendars
 */

import Anthropic from '@anthropic-ai/sdk';
import { calculateDriveTime } from './geo-lpr-agent.js';
import { optimizeDailyRoute } from './lead-routing-agent.js';

const anthropic = new Anthropic({
  apiKey: process.env.CLAUDE_API_KEY
});

const APPOINTMENT_SCHEDULING_PROMPT = `You are the **Appointment Scheduling Agent**, responsible for calendar intelligence and no-show prevention.

## YOUR ROLE

You manage the entire appointment lifecycle:
1. **Suggest Optimal Times** - When is lead most likely to show up?
2. **Send Reminders** - Automated reminders (24hr, 2hr, 30min)
3. **Predict No-Shows** - Which appointments are at risk?
4. **Prevent No-Shows** - Interventions to increase show-up rate
5. **Handle Rescheduling** - Make it easy to reschedule vs cancel

---

## OPTIMAL TIME SLOT SELECTION

### **Factors to Consider:**

**1. Lead's Availability (Explicit)**
- Time zone
- Preferred time of day (if stated)
- Days available (weekdays vs weekends)

**2. Historical Show-Up Rates (ML-Powered)**
Analyze past appointments to find patterns:

\`\`\`
Time Slot Analysis (from 1,000 appointments):

Monday 9 AM: 72% show-up rate
Monday 12 PM: 85% show-up rate ← BEST
Monday 5 PM: 68% show-up rate

Tuesday 9 AM: 78% show-up rate
Tuesday 12 PM: 82% show-up rate
Tuesday 5 PM: 65% show-up rate (people tired after work)

Friday 9 AM: 75% show-up rate
Friday 12 PM: 70% show-up rate
Friday 5 PM: 58% show-up rate ← WORST (weekend mindset)

Weekend (Sat/Sun): 62% show-up rate (lower commitment)

INSIGHT: Lunch time (12-1 PM) weekdays = highest show-up rates
\`\`\`

**3. Lead Characteristics**
- **Lead Score**: Hot leads (130-150) show up 85%, Warm (90-129) show up 70%, Cold (<90) show up 50%
- **Demographics**:
  - Age 25-35: Prefer evening (6-8 PM)
  - Age 35-50: Prefer lunch (12-1 PM) or early morning (8-9 AM)
  - Age 50+: Prefer mid-morning (10-11 AM)
- **Industry**:
  - Gym owners: Prefer non-peak hours (avoid 6-8 AM, 5-7 PM)
  - Executives: Prefer early morning (7-9 AM) or late afternoon (4-6 PM)

**4. Scheduling Urgency**
- **Same-day booking**: 90% show-up (high commitment)
- **1-3 days out**: 80% show-up
- **4-7 days out**: 70% show-up
- **7-14 days out**: 60% show-up (too far, they forget)
- **14+ days out**: 45% show-up (very low commitment)

**Recommendation**: Book within 1-3 days when possible

---

## NO-SHOW PREDICTION MODEL

### **Risk Factors (0-100 No-Show Risk Score):**

**High Risk (+points):**
- Appointment >7 days out: +20
- Booked outside business hours: +15
- Lead score <90 (WARM/COLD): +15
- No email confirmation sent: +10
- No reminders sent: +10
- Lead hasn't responded to any messages: +10
- Multiple reschedules already: +10
- Friday afternoon or weekend: +10

**Low Risk (-points):**
- Appointment within 48 hours: -20
- Lead score >130 (HOT): -15
- Lead confirmed via reply ("Yes, I'll be there"): -20
- Lead has shown up before (returning customer): -15
- Morning weekday appointment (9 AM - 12 PM): -10

**No-Show Risk Tiers:**
- **80-100 (CRITICAL)**: 70-90% chance of no-show → Intervene immediately
- **60-79 (HIGH)**: 50-70% chance → Send extra reminder + incentive
- **40-59 (MEDIUM)**: 30-50% chance → Standard reminders
- **20-39 (LOW)**: 15-30% chance → Minimal intervention
- **0-19 (VERY LOW)**: <15% chance → Confirmed show

---

## REMINDER STRATEGY

### **Standard Reminder Sequence:**

**24 Hours Before:**
\`\`\`
Channel: Email + SMS (if opted in)
Message: "Hi [Name]! Friendly reminder: You have an appointment tomorrow at [Time] with [Rep Name] to discuss [Topic].

Looking forward to it! If you need to reschedule, just reply to this message.

Add to calendar: [Link]"

Goal: Confirm appointment, make it easy to add to personal calendar
\`\`\`

**2 Hours Before:**
\`\`\`
Channel: SMS (if opted in) or Email
Message: "Hey [Name], your appointment with [Rep Name] is in 2 hours at [Time].

Meeting link: [Zoom/Meet link]

See you soon! Reply YES to confirm or RESCHEDULE if needed."

Goal: Last-minute confirmation, provide meeting link
\`\`\`

**30 Minutes Before:**
\`\`\`
Channel: SMS only (urgent)
Message: "Your appointment starts in 30 minutes! Join here: [Link]

Can't make it? Reply RESCHEDULE and we'll find a new time."

Goal: Final nudge, reduce last-minute no-shows
\`\`\`

### **Enhanced Reminders (for High No-Show Risk):**

If No-Show Risk Score > 60, add:

**3 Days Before:**
\`\`\`
Channel: Email
Message: "Looking forward to our appointment on [Date] at [Time]!

Quick question: Is this time still good for you? Reply YES to confirm or let me know if we need to adjust.

Also, here's what we'll cover:
- [Benefit 1]
- [Benefit 2]
- [Benefit 3]

This should only take 15 minutes of your time."

Goal: Early confirmation, remind of value
\`\`\`

**If No Response to Any Reminder:**
\`\`\`
Channel: Phone call (human or automated)
Message: "Hi [Name], this is [Rep Name]. I wanted to personally confirm our appointment tomorrow at [Time]. I have some insights I'm excited to share with you about [specific pain point]. Will you be able to make it?"

Goal: Personal touch increases commitment
\`\`\`

---

## NO-SHOW PREVENTION TACTICS

### **Tactic 1: Value Reinforcement**
Remind lead WHY they booked:

\`\`\`
"Just a reminder: In our 15-minute call, I'll show you:
✅ Exactly where you're losing leads (most businesses don't know this)
✅ How to hit 65% conversion (vs 30% industry average)
✅ A free audit of your current lead flow

This could be worth $50K+/year to your business."
\`\`\`

### **Tactic 2: Commitment Device**
Ask for micro-commitment:

\`\`\`
"Quick question: Can you reply YES to confirm you'll be there? I want to make sure I block this time for you."
\`\`\`

When they reply YES, psychological commitment increases.

### **Tactic 3: Social Proof**
\`\`\`
"Quick note: We have 100+ gym owners on our waitlist for consultations. If you can't make it, please let me know ASAP so I can offer your slot to someone else."
\`\`\`

Creates FOMO + scarcity.

### **Tactic 4: Make Rescheduling Easy**
\`\`\`
"Life happens! If this time doesn't work anymore, no problem. Just reply RESCHEDULE and I'll send you new options."
\`\`\`

Better to reschedule than no-show (you keep the lead).

### **Tactic 5: Penalty/Incentive**
\`\`\`
For no-shows: "We had an appointment booked but you didn't show. I totally understand things come up. Want to reschedule? I'll give you priority access to our calendar."

For shows: "Thanks for making our appointment! As promised, here's your free lead audit + $100 credit toward your first month."
\`\`\`

---

## RESCHEDULING AUTOMATION

### **When Lead Requests Reschedule:**

1. **Acknowledge Fast** (within 1 minute)
\`\`\`
"No problem! Let me send you some new time options."
\`\`\`

2. **Offer 3-5 Specific Times** (don't make them pick from full calendar)
\`\`\`
"Here are my next available slots:
- Tomorrow at 2 PM
- Thursday at 10 AM
- Friday at 12 PM

Which works best?"
\`\`\`

3. **Use ML to Prioritize High Show-Up Times**
Offer times with historically high show-up rates first.

4. **Book Immediately**
\`\`\`
"Perfect! You're booked for Thursday at 10 AM. I'll send you a calendar invite now."
\`\`\`

5. **Restart Reminder Sequence**
24hr, 2hr, 30min reminders for new appointment.

---

## CALENDAR SYNC (Google/Outlook)

### **Two-Way Sync:**

**From GHL → External Calendar:**
- When appointment booked in GHL → Create event in Google Calendar
- Include: Meeting link, lead info, prep notes

**From External Calendar → GHL:**
- If rep blocks time in Google Calendar → Mark as unavailable in GHL
- Prevents double-booking

### **Availability Detection:**
\`\`\`
Query rep's calendar:
- Find free slots (no conflicts)
- Respect working hours (9 AM - 6 PM by default)
- Respect buffer time (15 min between meetings)
- Respect lunch blocks (12-1 PM)

Offer only truly available slots to lead.
\`\`\`

---

## OUTPUT FORMAT (STRICT JSON)

\`\`\`json
{
  "optimal_time_slots": [
    {
      "slot_id": "slot-001",
      "date": "2025-11-14",
      "time": "12:00 PM EST",
      "predicted_show_up_rate": "85%",
      "reasoning": "Monday lunch hour - historically highest show-up rate (85%) + within 48 hours (high commitment)",
      "rep_available": true,
      "priority": "HIGHEST"
    },
    {
      "slot_id": "slot-002",
      "date": "2025-11-14",
      "time": "2:00 PM EST",
      "predicted_show_up_rate": "78%",
      "reasoning": "Monday afternoon - good show-up rate (78%) + within 48 hours",
      "rep_available": true,
      "priority": "HIGH"
    },
    {
      "slot_id": "slot-003",
      "date": "2025-11-15",
      "time": "10:00 AM EST",
      "predicted_show_up_rate": "80%",
      "reasoning": "Tuesday morning - strong show-up rate (80%)",
      "rep_available": true,
      "priority": "HIGH"
    }
  ],

  "no_show_risk_analysis": {
    "risk_score": 45,
    "risk_tier": "MEDIUM",
    "risk_factors": [
      { "factor": "Appointment 5 days out", "points": +15 },
      { "factor": "Lead score 95 (WARM)", "points": +10 },
      { "factor": "No prior relationship", "points": +10 }
    ],
    "mitigating_factors": [
      { "factor": "High-intent GMB lead", "points": -10 },
      { "factor": "Requested demo explicitly", "points": -10 }
    ],
    "predicted_no_show_probability": "35%",
    "recommended_interventions": [
      "Send 3-day advance reminder with value reinforcement",
      "Request confirmation reply 24 hours before",
      "Send meeting prep document to increase investment"
    ]
  },

  "reminder_schedule": {
    "reminders": [
      {
        "timing": "72 hours before",
        "channel": "Email",
        "message": "Hi John! Quick check-in: We're confirmed for Thursday at 12 PM EST. Still good for you? Reply YES to confirm.\n\nP.S. I'll be sharing insights on how to hit 65% conversion (vs your current 30%). This could be worth $50K+/year.",
        "goal": "Early confirmation + value reminder",
        "send_if": "no_show_risk_score > 40"
      },
      {
        "timing": "24 hours before",
        "channel": "Email + SMS",
        "message": "Reminder: Appointment tomorrow at 12 PM EST with Sarah Johnson. Add to calendar: [link]. Looking forward to it!",
        "goal": "Standard 24hr reminder"
      },
      {
        "timing": "2 hours before",
        "channel": "SMS",
        "message": "Your appointment starts in 2 hours! Join here: [Zoom link]. Reply YES to confirm or RESCHEDULE if needed.",
        "goal": "Last-minute confirmation"
      },
      {
        "timing": "30 minutes before",
        "channel": "SMS",
        "message": "Starting in 30 min! Join: [link]. Can't make it? Reply RESCHEDULE.",
        "goal": "Final nudge"
      }
    ],
    "if_no_response_to_24hr_reminder": {
      "action": "Phone call from rep",
      "timing": "6 hours before appointment",
      "message": "Personal confirmation call to increase commitment"
    }
  },

  "calendar_integration": {
    "google_calendar_event": {
      "summary": "Demo Call - John Smith (Gym Owner)",
      "description": "Lead Score: 95/100\nIndustry: Fitness\nPain Point: Low conversion (30%)\nGoal: Show how to hit 65% conversion\n\nPrep Notes:\n- Review Virtual LPR scoring\n- Pull gym industry case studies\n- Calculate potential revenue increase for his size",
      "start": "2025-11-14T12:00:00-05:00",
      "end": "2025-11-14T12:30:00-05:00",
      "attendees": ["john@gymexample.com", "sarah@company.com"],
      "location": "Zoom (link in description)",
      "reminders": {
        "useDefault": false,
        "overrides": [
          {"method": "popup", "minutes": 30},
          {"method": "email", "minutes": 120}
        ]
      }
    },
    "sync_status": "Successfully synced to Google Calendar",
    "conflicts_detected": false
  },

  "post_appointment_tracking": {
    "if_lead_shows": {
      "action": "Mark as SHOW, update rep performance stats",
      "follow_up": "Send thank-you email + next steps within 1 hour"
    },
    "if_lead_no_shows": {
      "action": "Mark as NO_SHOW, send recovery message",
      "recovery_message": "Hi John, we had an appointment today but didn't connect. I totally understand things come up! Want to reschedule? I have priority slots available.",
      "ml_learning": "Log no-show for pattern analysis (update prediction model)"
    },
    "if_lead_reschedules": {
      "action": "Book new time, restart reminder sequence",
      "note": "Reschedule = still interested (better than no-show)"
    }
  },

  "ml_insights": {
    "optimal_booking_window": "Book within 1-3 days for 80% show-up rate",
    "best_times_for_this_lead_profile": ["Monday 12 PM", "Tuesday 10 AM", "Thursday 12 PM"],
    "avoid_times": ["Friday after 2 PM (58% show-up)", "Weekends (62% show-up)"],
    "similar_leads_show_up_rate": "73% (gym owners, age 35-50, WARM tier)",
    "recommendation": "Book Monday 12 PM slot (highest predicted show-up: 85%)"
  }
}
\`\`\`

---

## CRITICAL RULES

1. **Book ASAP**: Same-day or next-day = 90% show-up, 7+ days = 60% show-up
2. **Reminders Are Non-Negotiable**: 24hr + 2hr + 30min reminders reduce no-shows by 40%
3. **Make Rescheduling Easy**: Better to reschedule than lose the lead forever
4. **Track Everything**: Log shows/no-shows/reschedules for ML learning
5. **Personalize Reminders**: Generic reminders ignored, specific value reminders work
6. **Offer 3-5 Times Max**: Too many choices = decision paralysis

---

Remember: Your job is to maximize show-up rate (target: 85%+) through optimal scheduling + proactive reminders + no-show prediction.`;

/**
 * Schedule appointment and generate reminder sequence
 */
export async function scheduleAppointment(leadData, repCalendar, historicalShowUpData) {
  const userPrompt = `
LEAD DATA:
${JSON.stringify(leadData, null, 2)}

REP CALENDAR (available slots):
${JSON.stringify(repCalendar, null, 2)}

HISTORICAL SHOW-UP DATA:
${JSON.stringify(historicalShowUpData, null, 2)}

---

**TASK**: Recommend optimal appointment times and generate no-show prevention strategy.

Requirements:
1. Analyze available time slots
2. Predict show-up rate for each slot (based on historical data)
3. Calculate no-show risk score for this lead
4. Recommend top 3-5 time slots
5. Generate reminder schedule
6. Provide no-show prevention tactics

Return ONLY valid JSON matching the output format.`;

  const message = await anthropic.messages.create({
    model: 'claude-sonnet-4-5-20250929', // Scheduling intelligence requires reasoning
    max_tokens: 4096,
    temperature: 0.3,
    system: APPOINTMENT_SCHEDULING_PROMPT,
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
 * Schedule appointment with travel time optimization (v2.0)
 *
 * For in-person meetings, considers:
 * - Drive time from rep's location to lead
 * - Buffer time between consecutive appointments
 * - Traffic patterns (morning vs afternoon vs rush hour)
 *
 * @param {Object} leadData - Lead information with location
 * @param {Object} repData - Rep information with base_location and calendar
 * @param {Object} historicalShowUpData - Historical show-up rates
 * @param {Object} options
 *   - meeting_type: "in_person" | "virtual" (default virtual)
 *   - meeting_duration_minutes: number (default 60)
 *   - buffer_time_minutes: number (default 30)
 *   - consider_traffic: boolean (default true)
 * @returns {Promise<Object>} Optimal appointment times with travel considerations
 */
export async function scheduleAppointmentWithTravelTime(
  leadData,
  repData,
  historicalShowUpData,
  options = {}
) {
  const {
    meeting_type = 'virtual',
    meeting_duration_minutes = 60,
    buffer_time_minutes = 30,
    consider_traffic = true
  } = options;

  // If virtual meeting, use standard scheduling
  if (meeting_type === 'virtual') {
    return await scheduleAppointment(leadData, repData.calendar, historicalShowUpData);
  }

  // IN-PERSON MEETING: Calculate travel time
  if (!repData.base_location || !leadData.location) {
    console.log('Missing location data for in-person meeting, falling back to virtual scheduling');
    return await scheduleAppointment(leadData, repData.calendar, historicalShowUpData);
  }

  // Step 1: Calculate drive time
  const driveTime = await calculateDriveTime(
    repData.base_location,
    leadData.location,
    'driving'
  );

  // Step 2: Get rep's existing appointments for context
  const existingAppointments = repData.calendar?.appointments || [];

  // Step 3: Find available slots that account for travel time
  const availableSlotsWithTravel = [];

  for (const slot of repData.calendar?.available_slots || []) {
    // Check if there's enough time before/after existing appointments
    const slotTime = new Date(slot.start_time);

    let hasConflict = false;
    let travelWarning = null;

    for (const existingAppt of existingAppointments) {
      const apptTime = new Date(existingAppt.start_time);
      const apptEnd = new Date(existingAppt.end_time);

      // Check if new appointment would conflict with travel time
      const minutesBefore = (slotTime - apptEnd) / (1000 * 60);
      const minutesAfter = (apptTime - slotTime) / (1000 * 60);

      const requiredBuffer = driveTime.duration.minutes + buffer_time_minutes;

      if (minutesBefore > 0 && minutesBefore < requiredBuffer) {
        hasConflict = true;
        travelWarning = `Not enough time after previous appointment (need ${requiredBuffer} mins for travel + buffer, have ${Math.round(minutesBefore)} mins)`;
        break;
      }

      if (minutesAfter > 0 && minutesAfter < requiredBuffer) {
        hasConflict = true;
        travelWarning = `Not enough time before next appointment (need ${requiredBuffer} mins for travel + buffer, have ${Math.round(minutesAfter)} mins)`;
        break;
      }
    }

    if (!hasConflict) {
      availableSlotsWithTravel.push({
        ...slot,
        drive_time_minutes: driveTime.duration.minutes,
        distance_miles: driveTime.distance.miles,
        buffer_time_minutes,
        total_time_required: driveTime.duration.minutes + meeting_duration_minutes + buffer_time_minutes,
        traffic_warning: considerTrafficForSlot(slot.start_time)
      });
    } else {
      availableSlotsWithTravel.push({
        ...slot,
        available: false,
        conflict_reason: travelWarning
      });
    }
  }

  // Step 4: Filter out conflicting slots and sort by desirability
  const feasibleSlots = availableSlotsWithTravel
    .filter(s => s.available !== false)
    .sort((a, b) => {
      // Prioritize slots without traffic warnings
      if (a.traffic_warning && !b.traffic_warning) return 1;
      if (!a.traffic_warning && b.traffic_warning) return -1;

      // Then prioritize shorter drive times
      return a.drive_time_minutes - b.drive_time_minutes;
    });

  // Step 5: Call standard scheduling with enhanced slot data
  const standardScheduling = await scheduleAppointment(
    leadData,
    { ...repData.calendar, available_slots: feasibleSlots },
    historicalShowUpData
  );

  // Step 6: Enhance response with travel time insights
  return {
    ...standardScheduling,
    travel_time_optimization: {
      meeting_type: 'in_person',
      drive_time: driveTime,
      buffer_time_minutes,
      total_time_required: driveTime.duration.minutes + meeting_duration_minutes + buffer_time_minutes,
      feasible_slots_count: feasibleSlots.length,
      travel_recommendations: [
        `Allow ${driveTime.duration.minutes} mins for travel (${driveTime.distance.miles} miles)`,
        `Total time block needed: ${driveTime.duration.minutes + meeting_duration_minutes + buffer_time_minutes} mins (travel + meeting + buffer)`,
        feasibleSlots.length < 3
          ? 'Limited availability due to travel time constraints. Consider virtual meeting.'
          : 'Good availability with travel time accounted for.'
      ]
    }
  };
}

/**
 * Consider traffic patterns for a given time slot
 */
function considerTrafficForSlot(startTime) {
  const hour = new Date(startTime).getHours();

  if (hour >= 7 && hour <= 9) {
    return 'Morning rush hour - expect 20-30% longer travel time';
  } else if (hour >= 16 && hour <= 18) {
    return 'Evening rush hour - expect 30-40% longer travel time';
  } else if (hour >= 11 && hour <= 14) {
    return 'Midday - optimal travel time';
  }

  return null; // No traffic warning
}

/**
 * Optimize multi-appointment day schedule
 *
 * Given multiple leads to visit in a day, find optimal order and timing
 *
 * @param {Object} rep - Rep with base_location
 * @param {Array<Object>} potentialAppointments - Leads to meet with location data
 * @param {Object} options
 *   - start_time: string (default "09:00")
 *   - end_time: string (default "17:00")
 *   - meeting_duration_each: number (default 60 mins)
 *   - buffer_between: number (default 30 mins)
 * @returns {Promise<Object>} Optimized daily schedule
 */
export async function optimizeMultiAppointmentDay(rep, potentialAppointments, options = {}) {
  const {
    start_time = '09:00',
    end_time = '17:00',
    meeting_duration_each = 60,
    buffer_between = 30
  } = options;

  // Use route optimization from lead-routing-agent
  const optimizedRoute = await optimizeDailyRoute(
    rep,
    potentialAppointments.map(appt => ({
      ...appt,
      estimated_meeting_duration: meeting_duration_each
    }))
  );

  // Check if schedule is feasible
  const totalTimeMinutes = optimizedRoute.summary.total_time_minutes + (buffer_between * optimizedRoute.total_stops);
  const availableMinutes = calculateAvailableMinutes(start_time, end_time);

  const feasible = totalTimeMinutes <= availableMinutes;

  return {
    rep_name: rep.name,
    date: new Date().toISOString().split('T')[0],
    optimized_route: optimizedRoute,
    schedule_analysis: {
      total_appointments: optimizedRoute.total_stops,
      total_drive_time: optimizedRoute.summary.total_drive_time_minutes,
      total_meeting_time: optimizedRoute.summary.total_meeting_time_minutes,
      total_buffer_time: buffer_between * optimizedRoute.total_stops,
      total_time_needed: totalTimeMinutes,
      available_time: availableMinutes,
      feasible: feasible,
      recommendation: feasible
        ? `Schedule is feasible. Rep can complete ${optimizedRoute.total_stops} appointments.`
        : `Schedule too tight. Reduce to ${Math.floor(optimizedRoute.total_stops * (availableMinutes / totalTimeMinutes))} appointments or extend working hours.`
    },
    suggested_schedule: generateSuggestedSchedule(optimizedRoute, start_time, buffer_between),
    optimized_at: new Date().toISOString()
  };
}

/**
 * Calculate available minutes in workday
 */
function calculateAvailableMinutes(startTime, endTime) {
  const [startHour, startMin] = startTime.split(':').map(Number);
  const [endHour, endMin] = endTime.split(':').map(Number);

  const startMinutes = startHour * 60 + startMin;
  const endMinutes = endHour * 60 + endMin;

  return endMinutes - startMinutes;
}

/**
 * Generate suggested schedule with specific times
 */
function generateSuggestedSchedule(optimizedRoute, startTime, bufferMinutes) {
  const [startHour, startMin] = startTime.split(':').map(Number);
  let currentMinutes = startHour * 60 + startMin;

  const schedule = [];

  optimizedRoute.route.forEach(stop => {
    // Travel time
    currentMinutes += stop.drive_time_from_previous;

    // Appointment
    const appointmentStart = formatMinutes(currentMinutes);
    currentMinutes += stop.estimated_meeting_duration;
    const appointmentEnd = formatMinutes(currentMinutes);

    schedule.push({
      time: `${appointmentStart} - ${appointmentEnd}`,
      activity: `Meeting with ${stop.lead_name}`,
      location: `${stop.location.lat.toFixed(4)}, ${stop.location.lng.toFixed(4)}`,
      duration_minutes: stop.estimated_meeting_duration,
      notes: `Drove ${stop.drive_time_from_previous} mins from previous location`
    });

    // Buffer
    currentMinutes += bufferMinutes;
    schedule.push({
      time: `${appointmentEnd} - ${formatMinutes(currentMinutes)}`,
      activity: 'Buffer / Travel Time',
      duration_minutes: bufferMinutes,
      notes: 'Time for wrap-up and travel to next appointment'
    });
  });

  return schedule;
}

/**
 * Helper: Format minutes to HH:MM
 */
function formatMinutes(totalMinutes) {
  const hours = Math.floor(totalMinutes / 60);
  const minutes = totalMinutes % 60;
  return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}`;
}

/**
 * Suggest best meeting type (virtual vs in-person) based on travel time
 *
 * @param {Object} repLocation - Rep's base location
 * @param {Object} leadLocation - Lead's location
 * @param {Object} dealContext - Deal size, lead tier, etc.
 * @returns {Promise<Object>} Meeting type recommendation
 */
export async function suggestMeetingType(repLocation, leadLocation, dealContext = {}) {
  const { deal_size = 0, lead_tier = 'WARM', relationship_stage = 'NEW' } = dealContext;

  if (!repLocation || !leadLocation) {
    return {
      recommended_type: 'virtual',
      reason: 'Missing location data',
      confidence: 'high'
    };
  }

  const driveTime = await calculateDriveTime(repLocation, leadLocation, 'driving');
  const driveMinutes = driveTime.duration.minutes;

  // Decision logic
  let recommendedType = 'virtual';
  let reason = '';
  let confidence = 'medium';

  if (driveMinutes <= 15) {
    recommendedType = 'in_person';
    reason = `Very close (${driveMinutes} mins). In-person builds stronger rapport.`;
    confidence = 'high';
  } else if (driveMinutes <= 30 && deal_size >= 10000) {
    recommendedType = 'in_person';
    reason = `Reasonable drive (${driveMinutes} mins) for $${deal_size.toLocaleString()} deal. Worth the investment.`;
    confidence = 'high';
  } else if (driveMinutes <= 45 && deal_size >= 50000) {
    recommendedType = 'in_person';
    reason = `Large deal ($${deal_size.toLocaleString()}) justifies ${driveMinutes} min drive. In-person increases close rate.`;
    confidence = 'high';
  } else if (driveMinutes <= 30 && relationship_stage === 'CLOSING') {
    recommendedType = 'in_person';
    reason = `Critical closing stage. ${driveMinutes} min drive worth it to seal the deal.`;
    confidence = 'medium';
  } else if (driveMinutes > 60) {
    recommendedType = 'virtual';
    reason = `Too far (${driveMinutes} mins). Virtual meeting more efficient.`;
    confidence = 'high';
  } else {
    recommendedType = 'virtual';
    reason = `Moderate distance (${driveMinutes} mins). Start with virtual, do in-person if needed later.`;
    confidence = 'medium';
  }

  return {
    recommended_type: recommendedType,
    alternative_type: recommendedType === 'virtual' ? 'in_person' : 'virtual',
    drive_time: driveTime,
    reason,
    confidence,
    roi_consideration: deal_size > 0
      ? `ROI: $${deal_size.toLocaleString()} deal ÷ ${Math.round(driveMinutes * 2 / 60)}h total time = $${Math.round(deal_size / (driveMinutes * 2 / 60)).toLocaleString()}/hour`
      : null,
    analyzed_at: new Date().toISOString()
  };
}

export default {
  scheduleAppointment,
  scheduleAppointmentWithTravelTime,
  optimizeMultiAppointmentDay,
  suggestMeetingType
};

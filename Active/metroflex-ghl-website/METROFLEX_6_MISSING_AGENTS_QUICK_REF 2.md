# MetroFlex 6 Missing Agents - Quick Reference

**Date:** November 15, 2025
**Status:** Ready for Development
**Data Source:** METROFLEX_COMPLETE_KB_V3.json ✅

---

## Overview

Based on the ecosystem analysis, we identified **6 missing agents** needed to complete the MetroFlex AI ecosystem. All required data is now available in V3 knowledge base.

**Current State:**
- ✅ 1 agent deployed: MetroFlex Events AI Chat Agent (Enhanced)
- ⏳ 6 agents identified: Ready for development

**Revenue Impact:**
- Current agent coverage: ~$125,000/year (19% of total)
- With all 7 agents: ~$655,000-715,000/year (100% of total)
- ROI: 5.2x increase in revenue coverage

---

## Agent 1: Licensing Prospect Qualification Agent

### Purpose
Qualify and nurture high-value licensing leads ($40,000-$60,000 per deal).

### Data Source
`METROFLEX_COMPLETE_KB_V3.json` → `metroflex_licensing` section

### Key Capabilities
1. **Qualification Scoring**
   - Assess liquid capital ($150k requirement)
   - Evaluate industry experience (3+ years preferred)
   - Review business plan completeness
   - Calculate licensing qualification score

2. **Package Recommendation**
   - New Build License ($60k) - for new gym construction
   - Rebrand License ($40k) - for existing gym rebranding
   - Beta program discount ($10k off for first 3 licensees)

3. **Application Guidance**
   - 8-step application process walkthrough
   - Document checklist (background check, proof of funds, business plan)
   - Territory analysis (10-mile radius for New Build, 7-mile for Rebrand)

4. **ROI Calculation**
   - Project revenue based on location, population density
   - Calculate ongoing fees (5% royalty capped at $2,500/month, $500 marketing fund)
   - Success story sharing (Ronnie Coleman, Branch Warren legacy)

### ML Model Integration
**Licensing Qualification Score**
- Inputs: liquid_capital, industry_experience_years, existing_gym_sqft, location_population_density, passion_score
- Output: 0-100 score (70+ = qualified, 85+ = fast-track)
- Purpose: Prioritize high-probability applicants

### High-Intent Triggers
- "open a metroflex gym"
- "franchise opportunity"
- "licensing cost"
- "how to become a licensee"
- "requirements to open gym"

### GHL Workflow Integration
1. Detect licensing inquiry → Capture lead to GHL
2. Tag: "Licensing - Hot Lead" (high-value)
3. Assign to: Brian Dobson
4. Follow-up: Phone interview within 24 hours
5. Pipeline stage: "Licensing Application - Qualification"

### Revenue Impact
- Deal value: $40,000-$60,000 per licensee
- Target: 2-3 deals in 2026 (Beta program)
- Scale: 6-10 deals by end of 2026
- Potential: $120,000-$600,000 in Year 1

---

## Agent 2: Gym Member Onboarding Agent

### Purpose
Convert prospects into MetroFlex Miami members and reduce churn through personalized onboarding.

### Data Source
`METROFLEX_COMPLETE_KB_V3.json` → `metroflex_gym_miami` section

### Key Capabilities
1. **Membership Consultation**
   - Assess workout frequency, budget, commitment level
   - Recommend tier: Founder's, Monthly, Annual, Day Pass, or 10-Pack
   - Calculate savings (Annual saves $169 vs monthly, 10-Pack saves $51)

2. **Founder's Membership Urgency**
   - Limited to first 100 members only
   - Deadline: May 15, 2026
   - Create FOMO messaging for high-value leads
   - Highlight: $2,500 one-time = LIFETIME access (no recurring fees)

3. **Facility Tour (Virtual)**
   - Describe equipment (dumbbells to 200 lbs, 6 Olympic platforms, Hammer Strength)
   - Highlight unique features (posing room, supplement shop, member lounge)
   - Compare to competitors

4. **Personal Training Upsell**
   - Single session: $80/hour
   - Package deals: 10-session ($70/hr), 20-session ($60/hr)
   - Contest prep special: 12-week package $2,400

5. **Grand Opening Hype**
   - June 1, 2026 (tentative)
   - Free workout day + meet & greet with Ronnie Coleman & Branch Warren
   - Build waitlist for Founder's Memberships

### ML Model Integration
**Churn Prediction Model**
- Inputs: membership_type, engagement_frequency (gym visits/week), event_participation, apparel_purchases, support_ticket_volume
- Output: 0-100 churn risk score (70+ = high risk)
- Purpose: Proactive retention campaigns (special offers, check-ins)

### High-Intent Triggers
- "join metroflex miami"
- "membership prices"
- "founder's membership"
- "when does miami open"
- "personal training"
- "day pass"

### GHL Workflow Integration
1. Detect membership inquiry → Capture lead to GHL
2. Tag: "Miami Gym - Prospect" (high-value if Founder's interest)
3. Pipeline stage: "Membership - Consideration"
4. Automated follow-up sequence:
   - Day 1: Welcome email with facility photos
   - Day 3: Founder's Membership scarcity reminder (XX/100 left)
   - Day 7: Grand opening event invitation
   - Day 14: Limited-time offer (if applicable)

### Revenue Impact
- Founder's Memberships: $2,500 x 100 = $250,000 (one-time, high priority)
- Monthly/Annual: $89-899 x 200-300 members = $150,000+/year recurring
- Personal Training: $50,000+/year
- **Total Year 1 Potential:** $450,000+

---

## Agent 3: Ticket Sales & Spectator Agent

### Purpose
Sell spectator tickets via TicketSpice and maximize family engagement at events.

### Data Source
`METROFLEX_COMPLETE_KB_V3.json` → `ticketing` section

### Key Capabilities
1. **Ticket Recommendations**
   - Assess group size, budget, seating preference
   - Recommend: General Admission ($25), VIP ($75), Weekend Pass ($40), Family Pack ($80)
   - Highlight: Kids 12 and under free with paid adult

2. **Group Booking Coordination**
   - 10+ spectators = 15% discount
   - Provide group booking codes
   - Coordinate with brian@metroflexgym.com

3. **TicketSpice Integration**
   - Guide to event-specific URLs (ticketspice.com/metroflex-ronnie-coleman-2026)
   - Explain QR code e-ticket delivery
   - Clarify: Spectator tickets ≠ competitor registration (separate systems)

4. **Competitor Perks**
   - Remind competitors: 2 complimentary spectator passes for family/friends
   - No need to purchase if competing

5. **Refund/Transfer Policy**
   - Tickets non-refundable but transferable
   - Contact brian@metroflexgym.com up to 48 hours before event

### ML Model Integration
None directly, but feeds into:
- **Event Attendance Prediction Model** (spectator ticket sales = leading indicator)
- **Lead Scoring Model** (family engagement = higher lifetime value)

### High-Intent Triggers
- "buy tickets"
- "spectator tickets"
- "VIP seating"
- "bring my family"
- "group tickets"
- "how much are tickets"

### GHL Workflow Integration
1. Detect ticket inquiry → Capture lead to GHL
2. Tag: "Spectator - Ticket Interest"
3. Pipeline stage: "Event Attendance - Spectator"
4. Automated follow-up:
   - Day 1: TicketSpice URL with direct link
   - Day 7: Event reminder (if ticket purchased)
   - Day before event: Arrival instructions + parking info

### Revenue Impact
- 3 events/year x 500-2,000 spectators x $25-75/ticket
- Conservative: $25,000/year
- Optimistic (with growth): $50,000+/year

---

## Agent 4: Apparel Recommendation Agent

### Purpose
Recommend MetroFlex apparel products, suggest sizing, and drive e-commerce sales.

### Data Source
`METROFLEX_COMPLETE_KB_V3.json` → `metroflex_apparel` section

### Key Capabilities
1. **Product Catalog Search**
   - 8 SKUs: Tees, Tanks, Hoodies, Shorts, Hats, Gym Bags, Wrist Wraps, Lifting Belts
   - Filter by: category, price, color, availability
   - Show stock status (most items in stock, lifting belt restocks 3/1/26)

2. **AI Size Recommendation**
   - Inputs: height, weight, preferred fit (tight/regular/loose)
   - Model: Size Recommendation ML Model
   - Output: Recommended size (S/M/L/XL/2XL/3XL)

3. **Cross-Sell & Upsell**
   - Bundle suggestions: "Competitors often buy tee + wrist wraps + gym bag"
   - Free shipping reminder: "Add $XX more to qualify for free shipping over $75"

4. **Multi-Channel Sales**
   - Online: metroflexapparel.com (launches Feb 15, 2026)
   - In-person: Arlington gym front desk
   - Events: Pop-up shop at all championships

5. **Wholesale Inquiries**
   - Detect gym/retailer interest → Route to brian@metroflexgym.com
   - Mention wholesale pricing available

### ML Model Integration
**Size Recommendation Model**
- Inputs: height (inches), weight (lbs), preferred_fit, product_category
- Output: Recommended size
- Purpose: Reduce returns, improve satisfaction

### High-Intent Triggers
- "buy shirt"
- "metroflex apparel"
- "order hoodie"
- "gym bag"
- "where to buy merch"
- "apparel sizing"

### GHL Workflow Integration
1. Detect apparel interest → Capture lead to GHL
2. Tag: "Apparel - Shopper"
3. Pipeline stage: "E-Commerce - Browsing"
4. Abandoned cart recovery:
   - If user doesn't complete purchase within 24 hours → Reminder email
   - Offer: 10% discount code for first-time buyers

### Revenue Impact
- Target: $120,000 Year 1 (from roadmap)
- Average order value: $60-80
- Target: 1,500-2,000 orders/year
- Repeat customer rate: 30%+

---

## Agent 5: Event Fulfillment & Day-Of Agent

### Purpose
Coordinate day-of logistics for competitors, spectators, and vendors.

### Data Source
`METROFLEX_COMPLETE_KB_V3.json` → Combined from `metroflex_events`, `ticketing`, `vendor_booths`

### Key Capabilities
1. **Competitor Day-Of Support**
   - Arrival time guidance (check MuscleWare confirmation email)
   - Weigh-in procedures
   - Music upload reminders (48-72 hours before)
   - Backstage logistics

2. **Spectator Check-In**
   - QR code scanning instructions
   - Parking information
   - Venue layout (seating, vendor expo, restrooms)
   - Schedule of events (prejudging vs finals)

3. **Vendor Coordination**
   - Load-in times (Friday 2-8 PM)
   - Setup instructions (10x10, 10x20, 20x20 booth layouts)
   - Power access, table/chair delivery
   - Load-out procedures (immediately after awards)

4. **Real-Time Issue Resolution**
   - Music playback issues → Contact tech team
   - Lost credentials → Reprint at check-in desk
   - Vendor no-show → Alert event coordinator
   - Medical emergencies → Direct to on-site paramedics

5. **Post-Event Follow-Up**
   - Results posting (npcnewsonline.com)
   - Photo gallery links (Physique Visuals)
   - Feedback survey
   - Next event promotion

### ML Model Integration
**Event Attendance Prediction Model**
- Inputs: historical_attendance, marketing_spend, divisions_offered, sponsorship_level, social_media_engagement
- Output: Predicted competitor + spectator count
- Purpose: Resource allocation (staff, seating, parking)

### High-Intent Triggers
- "what time should I arrive"
- "where do I check in"
- "how do I upload music"
- "parking information"
- "vendor load-in"
- "backstage access"

### GHL Workflow Integration
1. Day-of inquiries → Real-time SMS responses (GHL SMS automation)
2. Tag: "Event Day - Active Participant"
3. Post-event:
   - Survey automation (NPS score)
   - Next event registration reminder (early bird pricing)

### Revenue Impact
- Indirect: Improved event experience → Higher repeat registration rate
- Goal: 60%+ repeat competitor rate (vs industry avg 40%)
- Spectator satisfaction → Family referrals

---

## Agent 6: Sponsor Outreach & Qualification Agent

### Purpose
Qualify sponsor leads, present packages, and close high-value sponsorship deals.

### Data Source
`METROFLEX_COMPLETE_KB_V3.json` → `sponsorship_opportunities` section

### Key Capabilities
1. **Needs Assessment**
   - Company size, marketing budget, target audience
   - Goals: brand awareness, product sampling, lead generation
   - Past sponsorship experience

2. **Package Presentation**
   - Title Sponsor ($10k) - event naming rights, exclusive category
   - Platinum ($5k) - premium booth + stage logo
   - Gold ($2,500) - standard booth + social posts
   - Category Sponsor ($1,500) - division-specific activation

3. **ROI Justification**
   - Audience reach: 500-2,000 attendees per event
   - Social media exposure: 10,000+ followers across channels
   - Email list access: 3,000+ opt-in fitness enthusiasts
   - Press coverage: NPC News, local media

4. **Custom Package Creation**
   - Detect unique activation needs → Route to brian@metroflexgym.com
   - Examples: Product demo stage time, exclusive sampling rights

5. **Annual Sponsorship Upsell**
   - All 3 events: $20,000 (save $10,000 vs individual)
   - Year-round branding on metroflexevents.com
   - First right of refusal for 2027

### ML Model Integration
**Lead Scoring Model**
- Inputs: intent_detected (sponsorship), engagement_score, budget_indicators (mentions $10k+), timeline_urgency, authority_level (VP Marketing, Director)
- Output: 0-100 lead score (80+ = hot lead)
- Purpose: Prioritize high-probability closes

### High-Intent Triggers
- "sponsor"
- "sponsorship packages"
- "title sponsor"
- "brand exposure"
- "marketing opportunity"
- "sponsor the event"

### GHL Workflow Integration
1. Detect sponsorship inquiry → Capture lead to GHL
2. Tag: "Sponsorship - Hot Lead" (high-value)
3. Assign to: Brian Dobson
4. Pipeline stage: "Sponsorship - Qualification"
5. Follow-up sequence:
   - Day 1: Sponsorship deck PDF email
   - Day 3: Phone call to discuss packages
   - Day 7: Custom proposal (if needed)
   - Day 14: Contract + invoice

### Revenue Impact
- Current: ~$50,000/year from sponsorships
- Target with Agent 6: $100,000+/year
- Title Sponsors: 3 events x $10k = $30k minimum
- Platinum/Gold: 5-10 sponsors x $2,500-5,000 = $25-50k
- Annual packages: 1-2 x $20k = $20-40k

---

## 🚀 Development Priorities

### Phase 1: High-Value Agents (Weeks 1-4)
1. **Licensing Prospect Qualification Agent** ($40-60k per deal)
2. **Gym Member Onboarding Agent** ($2,500 Founder's Memberships)
3. **Sponsor Outreach & Qualification Agent** ($10k+ deals)

**Rationale:** Highest revenue per transaction, immediate impact

### Phase 2: Volume Agents (Weeks 5-8)
4. **Apparel Recommendation Agent** (e-commerce automation)
5. **Ticket Sales & Spectator Agent** (family engagement)

**Rationale:** Lower transaction value but higher volume, builds ecosystem

### Phase 3: Operational Excellence (Weeks 9-12)
6. **Event Fulfillment & Day-Of Agent** (satisfaction & retention)

**Rationale:** Improves experience, drives repeat business

---

## 📊 Combined Agent Ecosystem Metrics

### Revenue Coverage by Agent:

| Agent | Revenue Stream | Annual Value | Priority |
|-------|----------------|--------------|----------|
| **Events AI (existing)** | Competitor Registration | $75,000 | ✅ Live |
| **Licensing Agent** | Licensing Fees | $120-180k | 🔥 P1 |
| **Gym Member Agent** | Miami Memberships | $250,000 | 🔥 P1 |
| **Sponsor Agent** | Sponsorships | $100,000 | 🔥 P1 |
| **Apparel Agent** | Apparel Sales | $120,000 | ⚡ P2 |
| **Ticket Agent** | Spectator Tickets | $25,000 | ⚡ P2 |
| **Event Fulfillment Agent** | (Indirect retention) | N/A | ⏰ P3 |
| **TOTAL** | | **$690-750k** | |

### ML Model Deployment:

| Model | Used By | Data Source | Status |
|-------|---------|-------------|--------|
| Lead Scoring | Sponsor Agent, Licensing Agent | V3 KB notes | 📝 Documented |
| Churn Prediction | Gym Member Agent | V3 KB notes | 📝 Documented |
| Size Recommendation | Apparel Agent | V3 KB notes | 📝 Documented |
| Licensing Qualification | Licensing Agent | V3 KB notes | 📝 Documented |
| Attendance Prediction | Event Fulfillment Agent | V3 KB notes | 📝 Documented |

---

## 🛠 Technical Stack (All Agents)

### Backend:
- Python 3.11+
- OpenAI GPT-4o-mini (cost-optimized)
- ChromaDB (vector database for RAG)
- SentenceTransformers (embeddings)

### Integrations:
- GHL Webhooks (lead capture)
- TicketSpice API (ticket sales)
- MuscleWare (competitor registration - read-only)
- Shopify/WooCommerce (apparel e-commerce)

### Deployment:
- Docker containers (1 container per agent)
- Railway/Fly.io hosting
- NGINX reverse proxy
- PostgreSQL (agent state, conversation history)
- Redis (caching, session management)

### Monitoring:
- Prometheus (metrics)
- Grafana (dashboards)
- Loki (log aggregation)

---

## 📞 Next Actions

### For Development Team:
1. Review this quick reference document
2. Review METROFLEX_COMPLETE_KB_V3.json for detailed data
3. Start with Phase 1 agents (Licensing, Gym Member, Sponsor)
4. Use existing Events AI agent as template/framework
5. Deploy ML models in parallel

### For Brian/Noel:
1. Confirm priority order (P1, P2, P3)
2. Provide additional data if needed (e.g., competitor names for licensing partnerships)
3. Set up GHL pipelines for each agent's workflow
4. Review and approve agent personality/tone for brand consistency

---

**Document Version:** 1.0
**Last Updated:** November 15, 2025
**Status:** Ready for Development ✅

**Related Documents:**
- [METROFLEX_COMPLETE_KB_V3.json](AI_Agent/METROFLEX_COMPLETE_KB_V3.json) - Complete data source
- [METROFLEX_V3_KB_INTEGRATION_SUMMARY.md](AI_Agent/METROFLEX_V3_KB_INTEGRATION_SUMMARY.md) - Integration summary
- [METROFLEX_COMPLETE_ECOSYSTEM_ANALYSIS.md](../../../METROFLEX_COMPLETE_ECOSYSTEM_ANALYSIS.md) - Full ecosystem analysis

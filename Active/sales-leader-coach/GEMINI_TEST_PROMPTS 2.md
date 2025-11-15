# Gemini Gem - Test Prompts & Expected Outputs

Use these test prompts to verify your Sales Leader Coach Gem is working correctly.

---

## Test 1: Basic Conversation Analysis

### Input Prompt:
```
Date: 2025-10-15
Rep: Test Rep
Prospect: Jane Doe, VP Collections, ABC Credit Union
Stage: Discovery

Transcript:
Rep: Hi Jane, thanks for taking the time today.
Prospect: No problem. So what does your company do?
Rep: We provide vehicle location data to help with repossessions.
Prospect: Interesting. We're actually losing about $2 million a year to charge-offs.
Rep: That's significant. How are you currently locating vehicles?
Prospect: We use LexisNexis for skip tracing.
Rep: I see. Our system uses real-time license plate data.
Prospect: How much does it cost?
Rep: I'd need to put together a proposal. Can we schedule a follow-up?
Prospect: Sure.

Outcome: Scheduled follow-up call
```

### Expected Output Sections:
✅ **Conversation Analysis** with:
- Stage: Discovery
- Awareness Level: Problem Aware
- Engagement: High
- Grade: B or B-

✅ **What You Did Well** (2-4 items):
- Asked discovery question about current process
- Identified pain ($2M charge-offs)
- Secured follow-up meeting

✅ **What You Missed** (4-5 items):
- Did not quantify ROI ("At $2M in charge-offs, what's the average loss per vehicle?")
- Did not differentiate from LexisNexis strongly
- Did not qualify budget (BANT gap)
- Did not create urgency (cost of inaction)
- Did not secure concrete agenda for next call

✅ **Coached Response** (full script showing what to say)

✅ **Tactical Coaching** (specific gaps with "What to say" examples)

✅ **Next Conversation Goals** (3+ action items)

✅ **JSON Output** (properly formatted)

---

## Test 2: Objection Handling Query

### Input Prompt:
```
Prospect just said: "We already use LexisNexis for skip tracing and it works fine."

What should I say?
```

### Expected Output:
✅ Response should include:
- Challenger Sale reframe on stale data
- "Realternative data" terminology
- Specific language: "Credit bureau data is typically 6-12 months old by the time you act on it..."
- Differentiation: "We use real-time vehicle location data—where debtors are right now, not where they were"
- Side-by-side comparison offer: "Would it make sense to run a test?"

✅ Framework cited: Challenger Sale, CustomerCentric Selling

✅ Tone: Respectful, not bashing competitor

---

## Test 3: Product Knowledge Check

### Input Prompt:
```
Tell me about DRNsights Vehicle Search. What pain points does it solve and what are the key features?
```

### Expected Output:
✅ Pain points mentioned:
- High charge-off rates
- Can't find vehicles for repossession
- Recovery agents wasting time on bad addresses
- Hard-to-find ("elusive") vehicles

✅ Key features mentioned:
- Billions of real-time license plate detections
- Address scoring algorithm
- Up-to-date sighting summary (map/list view)
- Real-time alerts
- Repo system integration

✅ Proof points mentioned:
- "Billions of license plate detections" (scale)
- "Real-time" vs. stale DMV records (differentiation)
- "Intelligent scoring algorithm" (AI/ML capability)

✅ ROI anchor:
- "10% more recoveries = $X million saved annually"

---

## Test 4: Methodology Selection

### Input Prompt:
```
Prospect is in Discovery stage and is Problem Aware (knows they have a charge-off issue but doesn't know solutions exist). Which sales methodology should I use?
```

### Expected Output:
✅ Recommended methodologies:
- **Primary**: Gap Selling or SPIN Selling
- **Secondary**: Challenger Sale, Value Selling

✅ Rationale:
- Gap Selling: Quantify gap between current state ($2M charge-offs) and future state (reduced charge-offs)
- SPIN: Use Implication questions to build urgency ("What happens if this continues?")
- Challenger Sale: Teach them about real-time data vs. stale data

✅ Specific questions to ask:
- "What's your charge-off rate currently?"
- "What's the average loss per charge-off?"
- "Of those charge-offs, how many could have been recovered if you'd found the vehicle 30-60 days earlier?"

---

## Test 5: Batch Analysis (Multiple Conversations)

### Input Prompt:
```
--- CONVERSATION 1 ---
Date: 2025-10-15
Rep: John Smith
Prospect: Jane Doe, VP Collections, ABC Credit Union
Stage: Discovery
Transcript:
Rep: Hi Jane...
Prospect: We're losing $2M to charge-offs...
[abbreviated transcript]
Outcome: Scheduled follow-up

--- CONVERSATION 2 ---
Date: 2025-10-16
Rep: Sarah Johnson
Prospect: Bob Lee, CFO, XYZ Finance
Stage: Proposal
Transcript:
Rep: Thanks for reviewing the proposal...
Prospect: Budget is tight...
[abbreviated transcript]
Outcome: Pending decision

--- CONVERSATION 3 ---
Date: 2025-10-17
Rep: Mike Davis
Prospect: Lisa Chen, Collections Manager, 123 Bank
Stage: Discovery
Transcript:
Rep: Hi Lisa...
Prospect: Our contact rates are terrible...
[abbreviated transcript]
Outcome: No next steps

--- END ---
```

### Expected Output Sections:
✅ **Batch Analysis Summary**:
- Total Conversations: 3
- Date Range: Oct 15-17, 2025
- Avg Engagement Score
- Next-Step Conversion Rate: 67% (2/3)

✅ **Most Common Pain Points**:
- High charge-off rates (2/3 conversations, 67%)
- Low contact rates (1/3 conversations, 33%)

✅ **Most Common Objections**:
- Budget concerns (1/3, 33%)

✅ **Methodology Effectiveness** (if applicable based on sample)

✅ **Top Coaching Priorities**:
- Conversation 3 failed to secure next steps (needs coaching on call-to-action)
- Budget objection in Conversation 2 needs better handling

✅ **Playbook Updates**:
- "When prospect mentions 'charge-offs' → Immediately quantify with Gap Selling"

✅ **Individual Conversation Analyses** (all 3 conversations analyzed separately)

---

## Test 6: ROI Calculation

### Input Prompt:
```
Prospect has:
- $500M loan portfolio
- 5% charge-off rate
- Average loss per charge-off: $15,000

If Vehicle Search helps them recover 10% more vehicles, what's the ROI?
```

### Expected Output:
✅ Calculation shown:
```
Current charge-offs: $500M × 5% = $25M
Number of charge-offs: $25M ÷ $15,000 = 1,667 vehicles
10% recovery improvement: 167 additional vehicles recovered
Value saved: 167 × $15,000 = $2.5M per year

If Vehicle Search costs $100K/year:
ROI = $2.5M ÷ $100K = 25:1
```

✅ Presentation language:
"If we help you recover even 10% more vehicles before they charge off, that's $2.5 million in protected revenue per year. At a $100K investment, you're looking at a 25-to-1 ROI. That's a no-brainer."

---

## Test 7: Eugene Schwartz Awareness Level Detection

### Input Prompt:
```
Analyze this prospect's awareness level:

Prospect quote: "We're doing fine with our current process. I'm not really looking to make changes right now."
```

### Expected Output:
✅ **Awareness Level**: Unaware

✅ **Evidence**:
- "Doing fine" = doesn't recognize problem
- "Not looking to make changes" = no urgency
- Defensive posture

✅ **Recommended Approach**:
- Use Challenger Sale to educate on hidden costs
- Share statistics: "Most lenders don't realize they're spending $50K+ annually on avoidable impound fees"
- Create awareness: "Have you calculated what your current charge-off rate is costing you?"

✅ **Avoid**:
- Don't pitch product yet (they're not ready)
- Don't push for next steps (will trigger resistance)
- Focus on teaching, not selling

---

## Test 8: Cross-Sell Opportunity

### Input Prompt:
```
Prospect just bought Vehicle Search for repossession. What other DRNsights products should I cross-sell and why?
```

### Expected Output:
✅ **Primary Cross-Sell**: Skip Tracing

✅ **Rationale**:
- "A lot of accounts that end up in repo started in collections. If your collections team could reach the borrower earlier with Skip Tracing, you might avoid repossession entirely—which saves everyone time and money."

✅ **Secondary Cross-Sell**: Loss Alerts

✅ **Rationale**:
- "When you get a theft or impound alert from Loss Alerts, you can immediately use Vehicle Search to locate and recover the vehicle. They work together seamlessly."

✅ **Tertiary Cross-Sell**: Risk Scoring

✅ **Rationale**:
- "Risk Scoring helps you identify which accounts are most likely to go to repo in the first place, so you can prioritize your Vehicle Search efforts on high-risk accounts."

---

## Test 9: Humanization Check

### Input Prompt:
```
Rewrite this in a more human, conversational tone:

"As per our previous correspondence, I would be delighted to schedule a meeting at your earliest convenience to discuss the comprehensive suite of features our solution provides, including real-time data analytics, address verification algorithms, and integrated workflow management systems."
```

### Expected Output (Should Sound Human):
✅ **Good Examples**:
- "Thanks for getting back to me. Want to hop on a call this week? I'd love to show you how our real-time vehicle location data could help you recover more vehicles—it's pretty straightforward, and I think you'll see the value right away."
- "Hey, appreciate the reply. How about we schedule 30 minutes to walk through this? I'll show you the address scoring feature and how it helps your agents stop wasting trips. What works better for you—Tuesday or Thursday?"

✅ **Should NOT include**:
- "As per our previous correspondence"
- "I would be delighted"
- "At your earliest convenience"
- "Comprehensive suite of features"

✅ **Should include**:
- Contractions ("I'd," "you'll," "it's")
- Casual transitions ("Hey," "Thanks," "Want to")
- Simple language (not "comprehensive suite of features")

---

## Test 10: JSON Output Validation

### Input Prompt:
```
Provide ONLY the JSON output (no other text) for this conversation:

Date: 2025-10-15
Rep: Test Rep
Prospect: Sample Prospect, VP Collections, Test Bank
Stage: Discovery
Transcript: [Any simple conversation]
Outcome: Scheduled follow-up
```

### Expected Output:
✅ **Valid JSON** (can be parsed by `JSON.parse()` or `json.loads()`)

✅ **Required top-level keys**:
- `conversation_id`
- `conversation_metadata`
- `conversation_intelligence`
- `recommended_methodology`
- `product_mapping`
- `coached_response`
- `coaching_feedback`
- `salesforce_actions` (optional)

✅ **No syntax errors**:
- All brackets closed: `{ }`, `[ ]`
- All strings properly quoted: `"key": "value"`
- No trailing commas
- Valid escape characters

✅ **Test with validator**: Copy output to [jsonlint.com](https://jsonlint.com/) → Should pass validation

---

## Test 11: Statistics & Proof Points Accuracy

### Input Prompt:
```
What are the key statistics I should use when pitching Loss Alerts?
```

### Expected Output (Should Cite Correct Stats):
✅ **Impound Fees**:
- "$600+/month average impound fees" (DRN data)
- "If Loss Alerts saves you just $500/month in impound fees, it pays for itself"

✅ **Vehicle Theft**:
- "Over 2,000 vehicles stolen daily in the U.S." (Insurance Information Institute)
- "Know about theft before the borrower stops paying"

✅ **Accidents**:
- "Over 18,000 police-reported accidents daily" (U.S. DOT)
- "Stop trying to collect on vehicles that are already scrap metal"

✅ **Fraudulent Export**:
- "Tens of thousands of salvage titled vehicles illegally exported annually"
- "Stop fraudulent exports before your collateral is gone forever"

✅ **Social Proof**:
- Dade County Federal Credit Union testimonial: "The ability to get first-hand notifications of Loss Alerts electronically makes it less of a risk to the credit union"

---

## Test 12: Error Handling

### Input Prompt:
```
[Intentionally malformed conversation with missing fields]

Date: 2025-10-15
Transcript: Rep said something. Prospect said something else.
```

### Expected Output:
✅ **Graceful handling**:
- "I see you've provided a conversation, but I'm missing some context. Could you include:
  - Rep name
  - Prospect name, title, and company
  - Conversation stage (Discovery, Demo, Proposal, etc.)
  - Complete transcript (full dialogue)
  - Outcome

This will help me provide more accurate analysis."

✅ **Does NOT**:
- Crash or error out
- Provide generic analysis without acknowledging missing data
- Make up information

---

## Success Criteria

Your Gem is working correctly if:

✅ **Test 1-3**: Pass (core functionality)
✅ **Test 4-6**: Pass (methodology selection, ROI, product knowledge)
✅ **Test 7-9**: Pass (awareness detection, cross-sell, humanization)
✅ **Test 10**: Pass (valid JSON output)
✅ **Test 11**: Pass (accurate statistics cited)
✅ **Test 12**: Pass (error handling)

If any tests fail, review your Gemini setup:
1. Verify instructions file uploaded correctly
2. Verify all 8 reference files uploaded
3. Check Gem settings (response length, tone)
4. Refine instructions based on failure patterns

---

## Iterative Testing Workflow

1. **Run Tests 1-3** (basic functionality)
   - If pass → Continue to Tests 4-6
   - If fail → Debug instructions, re-upload files

2. **Run Tests 4-6** (intermediate functionality)
   - If pass → Continue to Tests 7-9
   - If fail → Check reference files, ensure Gem is accessing them

3. **Run Tests 7-9** (advanced functionality)
   - If pass → Continue to Tests 10-12
   - If fail → Refine tone guidelines, add examples to instructions

4. **Run Tests 10-12** (edge cases)
   - If pass → Gem is production-ready ✅
   - If fail → Add error handling and validation instructions

5. **Real-World Testing**
   - Analyze 5-10 actual sales conversations
   - Compare output to expectations
   - Refine instructions based on real-world performance

---

**Once all tests pass, your Gemini Gem is ready to coach world-class sales conversations!** 🎉

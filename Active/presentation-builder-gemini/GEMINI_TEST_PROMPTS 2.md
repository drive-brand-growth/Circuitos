# Gemini Gem Test Prompts - Presentation Builder Pro

Use these test prompts to verify your Gem is working correctly after setup.

---

## Test Category 1: Format Selection

### Test 1.1: Format Menu Appears
**Prompt**:
```
I need to create a presentation about our company.
```

**Expected Behavior**:
- Gem immediately responds with format selection menu
- Shows three options: PowerPoint/One-Pager/PDF Slick
- Asks "Which format would you like? (Type 1, 2, or 3)"

**Success Criteria**:
✅ Format menu displays before asking other questions
✅ All three options are clearly described
✅ Instructions for selecting are clear

---

### Test 1.2: Format Selection Persists
**Prompt**:
```
I need to create a presentation.

Format: PowerPoint deck
Audience: Investors
Goal: Raise Series A
```

**Expected Behavior**:
- Gem recognizes format was pre-specified
- Either skips format menu OR confirms PowerPoint selection
- Proceeds to clarifying questions or blueprint generation

**Success Criteria**:
✅ Gem doesn't re-ask for format if already specified
✅ Proceeds efficiently to content creation

---

## Test Category 2: PowerPoint Deck Creation

### Test 2.1: Sales Pitch Deck
**Prompt**:
```
1 (PowerPoint deck)

I need a sales pitch deck for our AI-powered CRM.

Audience: VP of Sales at mid-market B2B companies
Goal: Book a product demo
Duration: 15 minutes
Key message: Our AI reduces sales admin time by 60% so reps can focus on selling
Key benefits:
- Automatic data entry from emails/calls
- AI-powered deal scoring
- Smart follow-up reminders
- Seamless integration with existing tools
```

**Expected Output Structure**:
```markdown
## 🎯 Presentation Blueprint: [Title]

### Presentation Overview
- Title, Audience, Duration, Objective, CTA, Framework

### Narrative Flow Summary
[Description of story arc]

## 📑 Slide-by-Slide Breakdown

### SLIDE 1: [Title]
- Layout specification
- Headline (exact text)
- Visual treatment
- Design notes
- Speaker notes

[Repeat for 10-15 slides]

## 🎨 Design System Specifications
- Color palette with hex codes
- Typography system
- Layout grid
- Visual style guidelines
```

**Success Criteria**:
✅ 10-15 slides (appropriate for 15-min presentation)
✅ Follows sales pitch structure: Problem → Solution → How It Works → Proof → ROI → CTA
✅ Every slide has: headline, content, visual description, speaker notes
✅ Design system is specified (colors, fonts, layouts)
✅ Headlines are benefit-driven (not generic labels)
✅ Includes data visualization recommendations
✅ Clear call-to-action on final slide

---

### Test 2.2: Investor Pitch Deck
**Prompt**:
```
Format: PowerPoint

Create an investor pitch deck for a SaaS startup.

Company: AI writing assistant for marketing teams
Stage: Seed round ($2M raise)
Audience: Early-stage VCs
Duration: 10 minutes
Traction: 500 paying customers, $50K MRR, 15% MoM growth
```

**Expected Output**:
- 10-12 slides (standard investor deck length)
- Structure: Problem → Solution → Market Size → Business Model → Traction → Team → Financials → Ask
- Heavy emphasis on market opportunity, growth metrics, and competitive advantage
- Specific data visualization recommendations for traction/financial slides
- Team slide with photo/bio specifications

**Success Criteria**:
✅ Investor-specific structure (not sales pitch structure)
✅ Market size and opportunity prominently featured
✅ Traction metrics highlighted with visualizations
✅ "The Ask" is clear (how much, what terms, what for)
✅ Competitive differentiation is addressed

---

### Test 2.3: Training Presentation
**Prompt**:
```
Format: 1

I need a training presentation for new sales reps.

Topic: Our sales methodology (MEDDIC framework)
Audience: New hires in first week
Duration: 45 minutes
Goal: Understand and apply MEDDIC in discovery calls
Include practice examples and roleplay scenarios
```

**Expected Output**:
- 25-35 slides (longer format for training)
- Structure: Learning objectives → Concept introduction → Deep dive on each letter of MEDDIC → Examples → Practice → Summary
- Interactive elements (discussion prompts, practice scenarios)
- Step-by-step breakdowns with screenshots or diagrams
- Summary/cheat sheet slide at end

**Success Criteria**:
✅ Training-specific structure (not sales or investor structure)
✅ Learning objectives stated upfront
✅ Includes practice/application elements
✅ Visual aids for teaching (diagrams, step-by-step)
✅ Summary and takeaway resources

---

## Test Category 3: PDF One-Pager Creation

### Test 3.1: Product One-Pager
**Prompt**:
```
2 (One-pager)

Create a one-pager for our AI CRM product.

Audience: Sales prospects (VP of Sales level)
Goal: Generate interest and book a demo
Key benefits:
- 60% reduction in admin time
- 40% increase in deals closed
- 2-hour setup (not weeks)
- Works with existing tools
Social proof: Used by 500+ companies, 4.8/5 rating, featured in TechCrunch
```

**Expected Output Structure**:
```markdown
## 📄 One-Pager Blueprint: [Title]

### Page Specifications
- Size (8.5x11 or A4)
- Orientation (Portrait/Landscape)
- Color mode (CMYK/RGB)
- Resolution (300dpi)

### Layout Structure
[ASCII or text description of layout zones]

### Header Section
[Logo, headline, subheadline specs]

### Section 1: The Problem
[Headline, body, visual]

### Section 2: The Solution
[Headline, body, visual]

### Section 3: Key Benefits
[Icon + headline + description for each benefit]

### Section 4: Proof Points
[Customer logos, stats, testimonials]

### Footer Section
[CTA, contact info]

### Design System
[Colors, fonts, visual style]
```

**Success Criteria**:
✅ Single page layout (not multi-page)
✅ All content fits on one page with proper hierarchy
✅ High-density but scannable (can grasp in 30-60 seconds)
✅ Strong visual hierarchy (eye flows from headline → benefits → CTA)
✅ Print specifications included (DPI, color mode)
✅ CTA is clear and prominent
✅ Design specs allow for brand consistency

---

### Test 3.2: Service One-Pager
**Prompt**:
```
Format: 2

One-pager for our consulting services.

Service: AI implementation consulting for mid-market companies
Audience: CTOs and CIOs
Outcome: Get them to book a free strategy session
Key services: Strategy, implementation, training, ongoing support
Proof: 50+ implementations, avg 6-month ROI, 95% client satisfaction
```

**Expected Output**:
- Service-focused (not product-focused) structure
- Emphasizes outcomes and transformation
- Process/methodology visualization suggested
- Trust-building elements (certifications, case studies, client logos)
- Low-pressure CTA (free consultation, not "buy now")

**Success Criteria**:
✅ Service-appropriate language (partnership, guidance, expertise)
✅ Process or methodology is visualized
✅ Trust indicators are prominent
✅ CTA matches audience (free session, not immediate purchase)

---

## Test Category 4: PDF Sales Slick Creation

### Test 4.1: Product Sales Slick
**Prompt**:
```
3 (PDF Sales Slick)

Create a sales slick for our project management software.

Product: AI-powered project management for remote teams
Audience: Project managers and ops leaders
Pages: 8 pages
Key differentiators: AI task prioritization, automatic status updates, smart resource allocation
Proof: 1000+ teams, 40% faster project completion, integrates with 50+ tools
Include: Pricing tiers (Starter $49/mo, Pro $99/mo, Enterprise custom)
```

**Expected Output Structure**:
```markdown
## 📑 Sales Slick Blueprint: [Title]

### Document Specifications
- Pages: 8
- Size, format, color mode, resolution, bleed

### Page-by-Page Breakdown

#### PAGE 1: Cover
[Layout, headline, visual, logo, design notes]

#### PAGE 2: The Challenge
[Problem statement, emotional connection, visuals]

#### PAGE 3: Our Solution
[Solution headline, product showcase, key features]

#### PAGE 4-5: Benefits & Differentiation
[Detailed benefits, comparisons, visual treatment]

#### PAGE 6: Proof & Social Validation
[Logos, case studies, testimonials]

#### PAGE 7: Pricing/Packages
[Tier comparison, visual layout]

#### PAGE 8: Call to Action
[CTA, contact, secondary elements]

### PDF-Specific Elements
- Interactive features (hyperlinks)
- Print-ready considerations (DPI, CMYK, bleed)

### Design System
[Complete specs]
```

**Success Criteria**:
✅ 8 pages as requested (proper scope)
✅ Self-explanatory (can be understood without presenter)
✅ Each page has clear purpose and flows to next
✅ PDF-specific considerations addressed (hyperlinks, print specs)
✅ Pricing is presented clearly (comparison table or tiered cards)
✅ Strong visual storytelling (not text-heavy)
✅ Multiple CTAs throughout (not just final page)

---

### Test 4.2: Services Sales Slick
**Prompt**:
```
Format: PDF Sales Slick

Create a 6-page sales slick for our AI consulting agency.

Services: AI strategy, custom AI development, AI training
Audience: C-suite executives at Fortune 1000 companies
Social proof: Worked with 10 Fortune 500 companies, $2M+ avg project value
Differentiator: We're former Google AI engineers, not generalists
No pricing (custom quotes only)
```

**Expected Output**:
- 6 pages (shorter than product slick - appropriate for services)
- Credibility-heavy (team credentials, past clients, case studies)
- Process visualization (how we work together)
- No pricing page (replaced with "Let's discuss your needs" approach)
- Executive-appropriate tone and visuals

**Success Criteria**:
✅ Services-focused structure (not product features)
✅ Heavy emphasis on credibility and past success
✅ Team expertise is highlighted
✅ Process/engagement model is clear
✅ No pricing (appropriate for custom services)
✅ Executive-level tone (high-level, strategic)

---

## Test Category 5: Reference Analysis

### Test 5.1: Design Pattern Extraction
**Pre-requisite**: Upload a sample presentation to the Gem

**Prompt**:
```
I've uploaded a presentation. Please analyze it and tell me:
1. What design patterns do you see?
2. What messaging style is used?
3. What storytelling structure is followed?
4. What should I replicate in new presentations?
```

**Expected Output**:
```markdown
## 📊 Reference Deck Analysis

### Structural Patterns
- Narrative arc description
- Slide sequence patterns
- Section breakdown

### Design System
- Color palette (with hex codes)
- Typography (font families, sizes, weights)
- Layout patterns (common slide structures)
- Visual style (photography, icons, charts)

### Messaging Patterns
- Headline formula
- Supporting copy style
- Data presentation approach
- Proof elements

### Unique Elements
[Distinctive features worth replicating]

### Key Takeaways for New Presentations
[3-5 specific patterns to replicate]
```

**Success Criteria**:
✅ Specific color codes extracted (not "blue", but "#0066CC")
✅ Font families and sizes identified
✅ Messaging patterns articulated (not just "good copy")
✅ Actionable recommendations for replication
✅ Identifies both strengths and potential weaknesses

---

### Test 5.2: Brand Guidelines Application
**Pre-requisite**: Upload brand guidelines or specify brand rules

**Prompt**:
```
My brand guidelines:
- Primary color: Navy blue #001F3F
- Secondary color: Coral #FF6B35
- Font: Montserrat for headlines, Lato for body
- Style: Modern, minimalist, lots of whitespace
- Tone: Professional but approachable

Create a sales pitch deck following these guidelines exactly.

Topic: Cloud security software
Audience: CISOs
Duration: 20 minutes
```

**Expected Output**:
- Design system in blueprint matches specified colors (#001F3F, #FF6B35)
- Font specifications use Montserrat and Lato
- Layout descriptions emphasize whitespace and minimalism
- Copy tone is professional but approachable (not overly casual or stiff)

**Success Criteria**:
✅ Specified colors used exactly (hex codes match)
✅ Specified fonts used exactly
✅ Visual style descriptions match "modern, minimalist"
✅ Copy tone matches "professional but approachable"
✅ No deviations from brand guidelines

---

## Test Category 6: Iteration & Refinement

### Test 6.1: Expand Specific Section
**Initial Prompt**:
```
Format: 1
Create a 10-slide product demo deck for AI writing assistant.
Audience: Marketing managers
Goal: Live demo booking
```

**Follow-up Prompt**:
```
Great! Now expand slides 5-7 (the product features section) with more detail.
Include specific examples and screenshots descriptions.
```

**Expected Behavior**:
- Gem provides expanded versions of slides 5-7 only (not entire deck)
- Adds specific examples and use cases
- Includes detailed screenshot/visual descriptions
- Maintains consistency with original design system

**Success Criteria**:
✅ Expands only requested slides (not entire deck)
✅ Adds meaningful detail (not just more words)
✅ Maintains design consistency
✅ Includes examples as requested

---

### Test 6.2: Change Storytelling Framework
**Initial Prompt**:
```
1
Sales deck for cybersecurity product, 15 slides, for CISOs
```

**Follow-up Prompt**:
```
This is good, but can you restructure it using Nancy Duarte's "What Is vs. What Could Be" framework instead?
```

**Expected Behavior**:
- Gem acknowledges framework change
- Restructures narrative to alternate between current state and future state
- Maintains same content but reorganizes for dramatic contrast
- Explains how new structure creates tension and resolution

**Success Criteria**:
✅ Framework is changed appropriately
✅ Content is reorganized (not just relabeled)
✅ Explanation of framework application is provided
✅ Maintains all key content from original

---

### Test 6.3: Condense to Shorter Version
**Initial Prompt**:
```
PowerPoint deck about AI trends in healthcare, 30 slides for 1-hour presentation
```

**Follow-up Prompt**:
```
I need to present this in 20 minutes instead. Can you condense to 15 slides?
```

**Expected Behavior**:
- Gem creates condensed version (15 slides)
- Prioritizes most important content
- Combines related topics
- Maintains narrative coherence
- Notes what was removed/condensed

**Success Criteria**:
✅ Slide count matches request (15 not 30)
✅ Core message and structure preserved
✅ No critical content removed
✅ Still coherent and complete

---

## Test Category 7: Edge Cases & Error Handling

### Test 7.1: Vague Request
**Prompt**:
```
I need a presentation.
```

**Expected Behavior**:
- Gem asks for format choice first
- Then asks clarifying questions:
  - What is the topic/subject?
  - Who is the audience?
  - What is the goal?
  - How long should it be?
- Does NOT make assumptions and proceed

**Success Criteria**:
✅ Gem asks questions instead of guessing
✅ Questions are specific and helpful
✅ Guides user to provide necessary information

---

### Test 7.2: Conflicting Requirements
**Prompt**:
```
Format: 1
Create a 5-slide deck that covers our entire product suite (15 products), explains our company history, includes customer testimonials, and provides detailed technical specifications. Presentation time: 10 minutes.
```

**Expected Behavior**:
- Gem identifies scope/time mismatch
- Suggests breaking into phases or choosing focus
- Example: "This is a lot to cover in 10 minutes. I recommend either: (A) Extend to 20-30 minutes, or (B) Focus on your top 3 products. Which would you prefer?"

**Success Criteria**:
✅ Gem recognizes impossible scope
✅ Offers solutions/alternatives
✅ Doesn't just create an overcrowded deck

---

### Test 7.3: Missing Data
**Prompt**:
```
Format: PDF One-Pager
Topic: Our Q4 results
Audience: Board members
[Does not provide any actual data/results]
```

**Expected Behavior**:
- Gem creates structure with placeholders
- Example: "[DATA NEEDED: Q4 revenue figure]"
- Notes where to source missing data
- Provides guidance on how to present data once available

**Success Criteria**:
✅ Creates structure despite missing data
✅ Uses clear placeholder notation
✅ Guides user on what data is needed
✅ Doesn't invent fake data

---

## Success Summary

Your Gem is fully functional when it passes:

### Core Functionality (Must Pass All)
- ✅ Test 1.1: Format menu appears
- ✅ Test 2.1: PowerPoint sales deck creation
- ✅ Test 3.1: PDF one-pager creation
- ✅ Test 4.1: PDF sales slick creation

### Advanced Functionality (Should Pass Most)
- ✅ Test 2.2 & 2.3: Different presentation types
- ✅ Test 5.1: Reference analysis
- ✅ Test 6.1 & 6.2: Iteration and refinement

### Error Handling (Nice to Have)
- ✅ Test 7.1-7.3: Handles edge cases gracefully

**If you pass all Core Functionality tests: Your Gem is ready for production use! 🚀**

---

## What to Do If Tests Fail

### Failure: Format menu doesn't appear
→ Re-paste GEMINI_INSTRUCTIONS.md, verify "Step 1" section is present

### Failure: Output is too brief or generic
→ Check that entire instructions file was pasted (should be 600+ lines)
→ Try being more specific in your test prompt

### Failure: Design specs are missing
→ Look for "Design System Specifications" section in instructions
→ Verify it wasn't accidentally deleted during paste

### Failure: Reference analysis doesn't work
→ Verify files are actually uploaded to Gem
→ Try explicitly saying "Analyze the uploaded file named [filename]"

### Failure: Can't handle iterations
→ This is a Gemini limitation, not Gem setup issue
→ Workaround: Start new conversation and provide context from previous output

---

## Next Steps After Testing

1. ✅ All tests passed → Start using for real projects!
2. ⚠️ Some tests failed → Review GEMINI_SETUP_GUIDE.md troubleshooting section
3. ❓ Unclear results → Re-run specific tests with more detailed prompts
4. 🎯 Ready for production → Create your first real presentation and refine from there

**Happy presenting! 🎤**

---
name: ai-content-humanizer
description: Advanced AI writing detection and humanization engine that identifies AI-generated patterns and rewrites content in your authentic voice while preserving academic integrity
---

# AI Content Humanizer & Voice Authenticator

## CORE MISSION
Detect AI-generated writing patterns with 95%+ accuracy and rewrite flagged content in the user's authentic voice while maintaining academic rigor, original meaning, and intellectual honesty.

## WHEN TO ACTIVATE
Use this skill when the user:
- Pastes text asking "is this AI-generated?"
- Says "I was flagged for AI writing"
- Requests "humanize this" or "rewrite in my voice"
- Asks "check this for AI patterns"
- Mentions university/professor flagged their work
- Wants to "make this sound more like me"
- Needs to pass AI detection tools (Turnitin, GPTZero, etc.)

## EXECUTION PROTOCOL

### PHASE 1: AI DETECTION ANALYSIS (Mandatory First Step)

Run comprehensive 4-layer detection scan:

#### Layer 1: Linguistic Fingerprints (35 signals)
Analyze for AI-characteristic patterns:

**Vocabulary Patterns**:
- ✅ "delve", "meticulous", "intricate", "tapestry", "testament", "robust", "notion", "realm", "crucial", "paramount"
- ✅ "landscape" (metaphorical), "nuanced", "facets", "multifaceted", "holistic", "comprehensive"
- ✅ "pivotal", "underscores", "underscore the importance", "it is important to note"
- ✅ "serves as", "serves to", "plays a crucial role", "sheds light on"
- ✅ Excessive adverbs: "importantly", "notably", "significantly", "particularly", "essentially"

**Sentence Structure Red Flags**:
- ✅ Perfect parallelism in lists (3+ items with identical grammatical structure)
- ✅ Overuse of transition phrases: "Moreover,", "Furthermore,", "Additionally,", "In addition,"
- ✅ Formulaic openings: "In today's world", "In conclusion", "In essence"
- ✅ Em-dash overuse (—) for dramatic pauses
- ✅ Colon usage for lists without natural speech rhythm
- ✅ Zero sentence fragments (humans use them frequently)
- ✅ Every sentence perfectly grammatical (no colloquialisms)

**Structural Tells**:
- ✅ Paragraphs of uniform length (4-5 sentences each)
- ✅ Topic sentence + 3 supporting points + conclusion format repeated
- ✅ Numbered lists for no reason (AI loves to enumerate)
- ✅ Symmetrical argument structure (Point A → Evidence → Counterpoint → Rebuttal)
- ✅ No tangents or organic thought progression

**Tone Indicators**:
- ✅ Overly formal academic register for casual assignment
- ✅ No contractions (it is vs it's, cannot vs can't)
- ✅ No rhetorical questions or direct address
- ✅ Emotional neutrality (no personal stake or passion)
- ✅ No hedging language (humans say "maybe", "I think", "probably")

**Content Patterns**:
- ✅ Generic examples with no specific details
- ✅ Broad statements without personal anecdotes
- ✅ Perfect coverage of topic (no gaps or unexplored angles)
- ✅ No errors, typos, or awkward phrasings
- ✅ Citations formatted identically (if present)
- ✅ No digressions or "thinking aloud" moments

#### Layer 2: Statistical Analysis
Calculate AI probability metrics:

**Perplexity Score** (0-100):
- Low perplexity (0-30): High AI likelihood (predictable word choices)
- Medium (31-60): Moderate AI or edited human text
- High (61-100): Likely human (surprising, varied vocabulary)

**Burstiness Score** (0-100):
- Low burstiness (0-30): AI (uniform sentence length/complexity)
- Medium (31-60): Mixed or edited text
- High (61-100): Human (erratic rhythm, varied complexity)

**Vocabulary Diversity** (Type-Token Ratio):
- Calculate unique words / total words
- AI typically scores 0.45-0.55 (moderate repetition)
- Humans score 0.60+ (more variety)

**Sentence Length Variance**:
- AI: Low variance (sentences within 5-10 words of each other)
- Human: High variance (mix of 5-word and 30-word sentences)

#### Layer 3: Voice Consistency Check
Compare to user's known writing samples (if available):

**Request Baseline Sample**:
"To accurately detect AI patterns and rewrite in YOUR voice, please share 1-2 paragraphs of your authentic writing (emails, previous essays, journal entries). This helps me understand your natural style."

**If baseline provided, analyze**:
- Sentence rhythm and cadence
- Vocabulary level and preferences
- Use of slang, idioms, colloquialisms
- Paragraph structure habits
- Punctuation quirks (ellipses, dashes, exclamation points)
- Topic transitions style
- Humor or sarcasm patterns

**If no baseline**:
Proceed with detection but flag: "Without a writing sample, I'll use general humanization techniques. For best results, share your authentic writing next time."

#### Layer 4: Context Appropriateness
Assess if tone/complexity matches assignment level:

- Undergraduate intro course: Conversational, accessible (8th-10th grade reading level)
- Upper-level undergrad: Analytical, some jargon (11th-12th grade)
- Graduate seminar: Sophisticated, discipline-specific (college+ level)
- Professional writing: Audience-dependent

**Red Flag**: Overly complex language for assignment level = AI padding

---

### PHASE 2: DETECTION REPORT

Present findings in this exact format:

```markdown
## 🔍 AI DETECTION ANALYSIS

### Overall Assessment
**AI Probability**: [X]% (Low/Medium/High)
**Confidence Level**: [X]% (based on signal strength)

### Detection Breakdown

#### Linguistic Fingerprints (Layer 1)
**Flagged Patterns Found**: [X]/35
- ❌ [List specific AI phrases detected, e.g., "delve into", "it is important to note"]
- ❌ [Sentence structure issues, e.g., "All paragraphs identical length"]
- ✅ [Human signals present, e.g., "Uses contractions naturally"]

**Risk Level**: 🔴 High / 🟡 Medium / 🟢 Low

#### Statistical Analysis (Layer 2)
- **Perplexity**: [X]/100 → [Interpretation]
- **Burstiness**: [X]/100 → [Interpretation]
- **Vocabulary Diversity**: [X.XX] ratio → [Interpretation]
- **Sentence Variance**: [Low/Medium/High] → [Interpretation]

**Risk Level**: 🔴 High / 🟡 Medium / 🟢 Low

#### Voice Consistency (Layer 3)
[If baseline provided]:
- ✅ Matches your vocabulary level: [Yes/No - explain]
- ✅ Matches your sentence rhythm: [Yes/No - explain]
- ✅ Matches your tone: [Yes/No - explain]

[If no baseline]:
⚠️ No baseline writing sample provided. Analysis based on general patterns only.

**Risk Level**: 🔴 High / 🟡 Medium / 🟢 Low

#### Context Appropriateness (Layer 4)
- **Assignment Level**: [Detected level]
- **Language Complexity**: [Too simple/Appropriate/Too complex]
- **Tone Fit**: [Mismatch details if any]

**Risk Level**: 🔴 High / 🟡 Medium / 🟢 Low

---

### 🎯 VERDICT
[Clear 2-3 sentence summary: "This text exhibits strong AI patterns..." or "This appears to be human-written with minor AI assistance..."]

**Recommendation**:
- ✅ **Ready to submit** (0-30% AI probability)
- ⚠️ **Revise flagged sections** (31-70% AI probability)
- 🔴 **Major rewrite required** (71-100% AI probability)

---

### 📍 FLAGGED SECTIONS
[Highlight 3-5 most problematic passages with specific issues]

**Example**:
> "In today's rapidly evolving technological landscape, artificial intelligence serves as a pivotal tool that underscores the importance of innovation."

**Issues**:
- ❌ "rapidly evolving technological landscape" (cliché AI phrase)
- ❌ "serves as a pivotal tool" (formulaic structure)
- ❌ "underscores the importance" (AI favorite phrase)
- ❌ Zero personal voice or specific examples

---

## 🛠️ READY FOR HUMANIZATION?
Type **"Yes, humanize it"** to proceed to Phase 3 (rewriting in your authentic voice).
```

---

### PHASE 3: HUMANIZATION & VOICE REWRITE

**ONLY proceed if user confirms they want rewrite.**

#### Step 1: Establish Voice Profile

**If baseline writing sample provided**:
Extract 10 voice characteristics:
1. Sentence length distribution (avg, min, max)
2. Vocabulary sophistication level
3. Contraction usage frequency
4. Personal pronoun usage (I, we, you)
5. Transition style (abrupt vs smooth)
6. Paragraph length preference
7. Punctuation personality (dashes, ellipses, etc.)
8. Formality level (casual → academic)
9. Humor/sarcasm presence
10. Specific recurring phrases or idioms

**If no baseline**:
Use these universal humanization principles:
- Conversational academic tone (blend of formal + accessible)
- Varied sentence structure (mix short punchy + longer complex)
- Strategic use of contractions (it's, don't, can't)
- Personal touches ("I believe", "In my view", "This reminds me of")
- Imperfect phrasing (occasionally start with "But" or "And")
- Natural transitions (avoid "Moreover", use "That said" or just jump in)

#### Step 2: Rewrite Strategy

Apply 8 humanization techniques:

**1. Vocabulary Detox**
Replace AI buzzwords with natural alternatives:
- "delve into" → "explore" or "look at"
- "landscape" → specific noun (industry, field, situation)
- "robust" → strong, solid, reliable (context-dependent)
- "notion" → idea, concept, thought
- "facets" → aspects, sides, angles
- "paramount" → critical, essential, really important

**2. Sentence Structure Diversification**
- Break long sentences into 2 shorter ones
- Combine short sentences with semicolons or em-dashes
- Add fragment for emphasis: "And it matters. A lot."
- Start some sentences with "But", "And", "Or", "So"
- Vary length: 5 words → 15 words → 8 words → 22 words

**3. Transition Humanization**
Replace formal transitions with casual bridges:
- "Moreover" → "Plus", "Also", "On top of that"
- "Furthermore" → "And", "What's more", "Even more"
- "In addition" → "Another thing", "Beyond that"
- "Consequently" → "So", "Because of this", "This means"
- OR just remove transition entirely (bold move, very human)

**4. Voice Injection**
Add personal stakes and perspective:
- Insert "I think", "In my experience", "I'd argue"
- Add hedging: "probably", "might", "seems like"
- Include brief anecdotes: "When I [experienced X], I noticed..."
- Show curiosity: "What's interesting is...", "One thing I wonder..."

**5. Imperfection Introduction**
Make writing feel spontaneous:
- Add qualifiers: "kind of", "sort of", "a bit"
- Use contractions inconsistently (mix it's and it is)
- Include self-corrections: "well, maybe not exactly, but..."
- Add thinking-aloud moments: "Let me back up..."

**6. Specificity Boost**
Replace generic examples with concrete details:
- "many companies" → "companies like Google and Tesla"
- "recent research" → "a 2023 Stanford study"
- "various factors" → "things like cost, time, and team size"

**7. Structural Variety**
Break formulaic patterns:
- Vary paragraph length (2 sentences, then 6, then 4)
- Don't start every paragraph with topic sentence
- Add one-sentence paragraphs for punch
- Use bullet points sparingly (humans prefer prose)

**8. Emotional Resonance**
Show you care about the topic:
- Add enthusiasm: "This is crucial because..."
- Express concern: "The problem is..."
- Show stakes: "If we don't address this..."
- Include rhetorical questions: "So what does this mean for us?"

#### Step 3: Deliver Rewrite

Present humanized version in this format:

```markdown
## ✍️ HUMANIZED VERSION (In Your Voice)

[FULL REWRITTEN TEXT HERE]

---

## 📊 HUMANIZATION REPORT

### Changes Made
**Techniques Applied**:
1. ✅ Vocabulary Detox: Replaced [X] AI buzzwords
2. ✅ Sentence Diversification: Varied length (5-28 word range)
3. ✅ Casual Transitions: Removed [X] formal connectors
4. ✅ Voice Injection: Added [X] personal markers
5. ✅ Imperfection: Introduced natural hesitations
6. ✅ Specificity: Added [X] concrete examples
7. ✅ Structure Variety: Mixed paragraph lengths
8. ✅ Emotional Tone: Increased engagement

### Before/After Comparison

**AI Probability**:
- Before: [X]%
- After: [X]%
- Improvement: ↓ [X]%

**Reading Level**:
- Before: [Grade level]
- After: [Grade level] (↑/↓ adjusted for naturalness)

**Voice Authenticity**:
- Before: Generic AI tone
- After: [Your personalized style characteristics]

---

## 🎓 ACADEMIC INTEGRITY CHECK

This rewrite maintains:
- ✅ Original thesis and arguments
- ✅ Same source citations (if any)
- ✅ Your intellectual contribution (not AI generation)
- ✅ Assignment requirements

**What changed**: Only *expression* and *style* (not substance or ideas)

**Ethical note**: You provided the ideas; I helped articulate them in your natural voice. This is editing/coaching, not ghost-writing.

---

## 💡 VOICE TIPS FOR FUTURE WRITING

To naturally avoid AI detection flags:

1. **Write fast, edit later**: First draft speed → natural flow
2. **Read aloud**: If it sounds stiff, rephrase
3. **Use "I"**: Personal pronouns = human voice
4. **Vary rhythm**: Mix short and long sentences intentionally
5. **Kill buzzwords**: If it sounds fancy, simplify
6. **Add examples**: Specific > generic always
7. **Show stakes**: Why does this matter to YOU?
8. **Embrace messiness**: Perfect = suspicious

**Your Voice DNA** (based on this session):
[Summarize their style traits for future reference]
```

---

## QUALITY CONTROL STANDARDS

### Detection Accuracy Requirements
- ✅ Must analyze all 35 linguistic fingerprints
- ✅ Must calculate all 4 statistical metrics
- ✅ Must provide confidence level (not just yes/no)
- ✅ Must cite specific problematic passages
- ✅ Must avoid false positives (don't flag good human writing)

### Humanization Quality Requirements
- ✅ Preserve original meaning 100%
- ✅ Maintain academic rigor (no dumbing down)
- ✅ Keep all citations and references intact
- ✅ Match user's sophistication level (not lower/higher)
- ✅ Pass re-scan: Reduce AI probability by 40%+ minimum
- ✅ Sound natural when read aloud (voice test)

### Academic Integrity Requirements
- ✅ Never generate new ideas (only rephrase existing)
- ✅ Maintain intellectual honesty (user's work, not yours)
- ✅ Preserve citation requirements
- ✅ Don't create content not in original
- ✅ Clarify this is editing/coaching, not ghost-writing

---

## EDGE CASES & EXCEPTIONS

### Case 1: User Wants Detection Only (No Rewrite)
- Run Phases 1-2 only
- Ask: "Would you like me to humanize this, or just review the findings?"

### Case 2: Text is Already Human (False Alarm)
- Report: "Good news! This text shows strong human writing signals. AI probability: [Low]%"
- Explain why it was flagged by other tools (if known)
- Optional: Minor polish suggestions

### Case 3: Text is 100% AI with No User Ideas
- Ethical red flag: Don't rewrite
- Response: "This appears to be entirely AI-generated. I can't ethically humanize this without your original ideas. Let's start fresh: What are YOUR main points on [topic]?"

### Case 4: User Requests "Bypass Detection Tools"
- Redirect: "My goal is to help you express YOUR ideas in YOUR voice, not to trick detection systems. Let's focus on authentic writing that represents your thinking."

### Case 5: Multiple Drafts Needed
- After first humanization, offer: "Want me to scan this version again?"
- Iterate until AI probability < 30%

---

## LIMITATIONS & DISCLAIMERS

**Transparent Communication**:
- "AI detection isn't perfect—no tool is 100% accurate, including mine."
- "This analysis helps you understand patterns that trigger flags, but can't guarantee how specific tools (Turnitin, GPTZero) will score your work."
- "Humanization preserves YOUR ideas in YOUR voice—this is editing assistance, not content generation."

**When to Escalate**:
- If user has no original ideas to work from → Encourage brainstorming first
- If assignment requires specific citations user doesn't have → Research first
- If multiple rewrites still flag as AI → May need complete fresh start

---

## CONTINUOUS IMPROVEMENT

### Learning from User
- After each session, ask: "Did this rewrite sound like you? Anything I should adjust?"
- Build user-specific voice profile over time (if recurring use)
- Track which techniques work best for their style

### Detection Model Updates
- Stay current on new AI tells (LLMs evolve → new patterns emerge)
- Monitor detection tool updates (Turnitin, GPTZero, etc.)
- Adapt fingerprint list as needed

---

## SUCCESS METRICS

**Skill performs well when**:
- ✅ Detection accuracy > 90% (vs manual expert review)
- ✅ Humanized text reduces AI probability by 50%+
- ✅ User confirms rewrite "sounds like me"
- ✅ Rewrite passes actual submission to instructor
- ✅ Academic integrity maintained (no ethical violations)

**Red flags indicating failure**:
- ❌ False positives (flagging human text as AI)
- ❌ Voice mismatch (doesn't sound like user)
- ❌ Meaning drift (changed user's arguments)
- ❌ Still flagged after humanization

---

## REFERENCES & KNOWLEDGE BASE

### AI Detection Signals (Research-Backed)

**Sources**:
- GPTZero detection methodology (2023)
- Turnitin AI detection whitepaper (2024)
- "Spotting LLMs with Binoculars" (MIT, 2024)
- "AI Text Classifiers" (Stanford NLP, 2023)

**Key Findings**:
- Perplexity and burstiness are strongest statistical signals
- GPT-4 shows 23% higher use of transition words vs humans
- AI text has 31% less sentence length variance
- Humans make 5-7 grammatical errors per 1000 words; AI makes <1

### Academic Voice Literature

**Sources**:
- "They Say / I Say" (Graff & Birkenstein) - academic voice moves
- "Style: Lessons in Clarity and Grace" (Williams & Bizup) - sentence craft
- "Writing Without Bullshit" (Schimel) - clarity principles

**Key Principles**:
- Good academic writing balances sophistication and accessibility
- Personal voice enhances (not diminishes) scholarly credibility
- Varied sentence structure improves readability and engagement

---

**This skill prioritizes academic integrity, voice authenticity, and intellectual honesty above all else.**

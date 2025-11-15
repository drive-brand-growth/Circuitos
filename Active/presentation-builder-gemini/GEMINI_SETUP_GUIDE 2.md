# Gemini Gem Setup Guide - Presentation Builder Pro

**Time to Complete**: 5-10 minutes

---

## Prerequisites

- Google account with Gemini access
- Your reference presentations (optional but recommended):
  - Best sales decks (.pptx, .pdf)
  - Brand guidelines (.pdf)
  - Templates you want to replicate
  - Previous one-pagers or sales collateral

---

## Step 1: Create Your Gemini Gem (2 minutes)

### 1.1 Access Gemini Gems
1. Go to https://gemini.google.com/
2. Sign in with your Google account
3. Look for "Gems" in the left sidebar or top menu
4. Click "Gems" → "New Gem" or "Create Gem"

### 1.2 Name Your Gem
- **Recommended Name**: "Presentation Builder Pro"
- **Alternative Names**: "Deck Designer", "Pitch Deck AI", "Presentation Expert"
- Click to proceed to the instructions field

---

## Step 2: Install Instructions (2 minutes)

### 2.1 Copy Instructions File
1. Open the file `GEMINI_INSTRUCTIONS.md` in this folder
2. **Select ALL text** (Cmd+A or Ctrl+A)
3. **Copy** (Cmd+C or Ctrl+C)

### 2.2 Paste into Gemini
1. In your new Gem, find the "Instructions" field (large text area)
2. **Paste** the entire contents (Cmd+V or Ctrl+V)
3. Verify the paste was successful:
   - Should start with: "# Gemini Gem Custom GPT - Instructions"
   - Should end with: "**Let's build world-class presentations together.**"
   - Should be ~600+ lines

### 2.3 Save Your Gem
1. Click "Save" or "Create" button
2. Your Gem is now ready to use!

---

## Step 3: Upload Reference Materials (3 minutes - OPTIONAL)

**Why Upload References?**
- The Gem analyzes your best presentations to learn:
  - Your design style (colors, fonts, layouts)
  - Your messaging patterns (how you write headlines, structure content)
  - Your brand guidelines (logo usage, visual style)
  - Your storytelling approach (narrative flow, proof points)

### 3.1 Prepare Reference Files
Gather these files if you have them:

**High Priority**:
- [ ] Your best sales pitch deck (.pptx or .pdf)
- [ ] Company brand guidelines (.pdf)
- [ ] Any presentation template you want to replicate (.pptx)

**Medium Priority**:
- [ ] Recent successful presentations
- [ ] PDF one-pagers or sales slicks you like
- [ ] Competitor presentations you admire (for inspiration)

**Low Priority**:
- [ ] Training decks
- [ ] Webinar slides
- [ ] Conference presentations

### 3.2 Upload to Gemini Gem
**Note**: Gemini Gems may have file upload in the chat interface, NOT in the Gem setup itself.

**Method A - Upload During First Conversation**:
1. Start a conversation with your new Gem
2. Click the attachment/upload icon (paperclip or + symbol)
3. Upload your reference files
4. Say: "These are my reference presentations. Please analyze them and learn my design style and messaging patterns."

**Method B - Store in Gemini Drive**:
1. Upload files to your Google Drive
2. In your first conversation with the Gem, say: "I have reference presentations in my Drive at [share link]. Can you access them?"

**Method C - Copy/Paste Key Elements**:
If file upload isn't working:
1. Extract key elements manually (color codes, font names, design patterns)
2. Paste into first conversation: "Here are my brand guidelines: [paste details]"

### 3.3 Organize Your Reference Folder (Local Backup)
On your computer, save references in this structure:
```
presentation-builder-gemini/
└── reference/
    ├── pitch-decks/
    │   ├── 2024-sales-deck.pptx
    │   └── investor-pitch.pdf
    ├── brand/
    │   ├── brand-guidelines.pdf
    │   └── logo-files.zip
    ├── templates/
    │   └── slide-master-template.pptx
    └── one-pagers/
        ├── product-sheet.pdf
        └── sales-slick.pdf
```

---

## Step 4: Test Your Gem (3 minutes)

### 4.1 Basic Functionality Test

**Test 1: Format Selection**
Start a conversation with your Gem and type:
```
I need to create a presentation about our new product.
```

**Expected Response**:
The Gem should immediately ask you to choose a format:
```
I'll help you create a world-class presentation. First, please choose the format you need:

1. PowerPoint/Keynote/Google Slides Deck
2. PDF One-Pager
3. PDF Sales Slick

Which format would you like? (Type 1, 2, or 3)
```

✅ **PASS**: Gem asks for format choice
❌ **FAIL**: Gem skips format choice → Re-paste instructions and try again

---

**Test 2: PowerPoint Deck Creation**
Continue the conversation:
```
1 - PowerPoint deck

Audience: Sales prospects
Goal: Book a demo
Duration: 15 minutes
Topic: AI-powered CRM that reduces admin time
```

**Expected Response**:
The Gem should provide:
- Acknowledgment of requirements
- Possibly a few clarifying questions (if needed)
- Complete presentation blueprint including:
  - Slide-by-slide breakdown (10-15 slides for 15-min deck)
  - Headlines and body content for each slide
  - Visual treatment descriptions
  - Speaker notes
  - Design system specifications (colors, fonts)

✅ **PASS**: Gem provides structured, detailed blueprint
❌ **FAIL**: Generic or incomplete response → Check instructions pasted correctly

---

**Test 3: PDF One-Pager Creation**
Start a new conversation:
```
I need to create a one-pager for our AI CRM product.

Audience: VP of Sales
Goal: Get them to book a demo
Key benefits: 60% less admin time, 40% more deals closed, easy integration
```

**Expected Response**:
- Format selection menu (should ask for choice)
- After you select "2", should provide:
  - Page specifications (size, orientation, resolution)
  - Layout structure
  - Section-by-section breakdown (header, problem, solution, benefits, proof, CTA)
  - Design system
  - Print/digital guidance

✅ **PASS**: Gem provides complete one-pager blueprint
❌ **FAIL**: Response is incomplete or doesn't follow one-pager structure

---

**Test 4: Reference Analysis** (If you uploaded references)
Start a new conversation:
```
Please analyze my reference presentations and tell me what design patterns and messaging styles you see.
```

**Expected Response**:
The Gem should provide:
- Structural patterns (narrative arc, slide sequences)
- Design system (colors, typography, layouts)
- Messaging patterns (headline formulas, proof elements)
- Key takeaways to replicate

✅ **PASS**: Gem analyzes uploaded files and extracts patterns
❌ **FAIL**: "I don't see any files" → Upload files first, then try again

---

### 4.2 Advanced Tests

See [GEMINI_TEST_PROMPTS.md](GEMINI_TEST_PROMPTS.md) for comprehensive test cases.

---

## Step 5: Customize Your Gem (Optional)

### 5.1 Add Personality/Name
In the Gem settings, you can optionally:
- Set a custom greeting: "Hi! I'm Deck Designer. I'll help you create world-class presentations. What would you like to build today?"
- Add an avatar/icon

### 5.2 Create Shortcuts
If using Gemini regularly:
- Bookmark your Gem's URL
- Add to favorites
- Create desktop shortcut

### 5.3 Share with Team (If Applicable)
Some Gemini plans allow Gem sharing:
1. Click "Share" in your Gem settings
2. Set permissions (view/use)
3. Send link to team members

---

## Troubleshooting

### Issue 1: Gem Doesn't Ask for Format Choice

**Symptom**: Gem jumps straight to creating a presentation without asking PowerPoint/One-Pager/PDF choice

**Fix**:
1. Check that GEMINI_INSTRUCTIONS.md was pasted correctly
2. Look for the section starting with "**Step 1: Clarify & Confirm + Choose Format**"
3. Verify it contains the format selection menu
4. If missing, re-copy and re-paste instructions

---

### Issue 2: Gem Gives Generic/Short Responses

**Symptom**: Gem provides brief, unhelpful responses instead of detailed blueprints

**Possible Causes & Fixes**:

**Cause A: Instructions Not Pasted Correctly**
- Re-open GEMINI_INSTRUCTIONS.md
- Verify entire file is selected (should be 600+ lines)
- Re-paste into Gem instructions

**Cause B: Request Too Vague**
- Be more specific in your request
- Provide: audience, goal, duration/length, key message
- Example: "Create 15-slide sales deck for VPs targeting 60% admin reduction, goal: book demo"

**Cause C: Gemini Context Limit**
- If you've had a very long conversation, start a new chat
- Gemini may truncate responses in long threads

---

### Issue 3: Can't Upload Reference Files

**Symptom**: No file upload button or uploads fail

**Workaround Options**:

**Option 1: Manual Brand Guidelines**
Paste brand specs directly in first message:
```
Before we start, here are my brand guidelines:
- Primary color: #0066CC (blue)
- Secondary color: #FF6B35 (orange)
- Font: Helvetica Neue for headlines, Open Sans for body
- Style: Modern, clean, lots of whitespace
- Tone: Professional but conversational
```

**Option 2: Describe Your Best Deck**
```
I want to replicate the style of my best sales deck:
- Structure: Problem (slide 1) → Agitate (2-3) → Solution (4-6) → Proof (7-9) → CTA (10)
- Headlines: Benefit-driven statements (e.g., "Reduce Admin Time by 60%")
- Visuals: Full-bleed images with text overlays, minimal bullet points
- Color: Dark blue (#001F3F) with white text, orange (#FF6B35) accents
```

**Option 3: Upload Later**
- Set up Gem without references first
- Upload files in individual conversations as needed
- Ask Gem to remember patterns for future use

---

### Issue 4: Output Is Too Long/Short

**Too Long**:
```
That's great, but can you make it more concise? Aim for 10 slides instead of 20.
```

**Too Short**:
```
Can you expand this? I need more detail on slides 5-8, including speaker notes and visual treatments.
```

---

### Issue 5: Design Specs Don't Match My Brand

**Fix**:
```
Please revise the design system:
- Use [your colors]
- Use [your fonts]
- Follow [your visual style]
[Upload or paste your brand guidelines]
```

---

### Issue 6: Storytelling Framework Doesn't Fit

**Fix**:
```
Instead of [current framework], please use [preferred framework]:
- Nancy Duarte Story Arc
- Andy Raskin Strategic Narrative
- Problem-Agitate-Solve
- Hero's Journey
- AIDA (Attention-Interest-Desire-Action)
```

---

## Best Practices

### ✅ Do This:
- Be specific in your requests (audience, goal, length, key message)
- Upload your best reference presentations
- Test with simple requests first, then get more complex
- Iterate: "Expand slide 3", "Change the opening section", "Make it shorter"
- Save great outputs for future reference

### ❌ Don't Do This:
- Don't be vague: "Create a presentation about sales" (missing context)
- Don't expect actual files: Gem creates blueprints, not .pptx files
- Don't upload low-quality references: Garbage in, garbage out
- Don't give up after first try: Refine and iterate

---

## Next Steps

1. **Run Tests**: Complete the 4 tests in Step 4 above
2. **Detailed Testing**: Use [GEMINI_TEST_PROMPTS.md](GEMINI_TEST_PROMPTS.md) for comprehensive validation
3. **Create Real Presentation**: Start with a real project to test in production
4. **Refine**: Based on results, adjust your reference materials or request style
5. **Scale**: Once validated, use for all presentation needs

---

## Support

**Issue Not Listed Here?**
1. Check [GEMINI_TEST_PROMPTS.md](GEMINI_TEST_PROMPTS.md) for edge cases
2. Review [README.md](README.md) for comprehensive documentation
3. Re-read [GEMINI_INSTRUCTIONS.md](GEMINI_INSTRUCTIONS.md) to understand capabilities

**Gem Not Behaving as Expected?**
- Start a fresh conversation (long threads can confuse context)
- Re-paste instructions to ensure nothing was lost
- Verify you're using Gemini (not ChatGPT or Claude)

---

## Success Criteria

Your Gem is properly set up when:

✅ It asks for format choice (PowerPoint/One-Pager/PDF Slick) immediately
✅ It provides detailed, structured blueprints (not generic advice)
✅ It includes slide-by-slide or page-by-page breakdowns
✅ It specifies design systems (colors, fonts, layouts)
✅ It applies storytelling frameworks (Duarte, Raskin, PAS)
✅ It analyzes reference materials when provided
✅ It responds to refinement requests ("expand this", "make shorter")

**If all criteria are met: You're ready to build world-class presentations! 🚀**

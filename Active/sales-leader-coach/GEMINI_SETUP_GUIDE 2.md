# Gemini Gem Custom GPT - Complete Setup Guide

## Step-by-Step Setup (10 Minutes)

### Step 1: Create Your Custom GPT in Gemini

1. Go to [Google Gemini](https://gemini.google.com/)
2. Click **"Gems"** in the left sidebar
3. Click **"+ New Gem"**
4. Name it: **"Sales Leader Coach"**

---

### Step 2: Upload Instructions

1. Open **[GEMINI_INSTRUCTIONS.md](GEMINI_INSTRUCTIONS.md)** (in this folder)
2. **Copy the ENTIRE contents** of that file
3. In Gemini Gem, paste into the **"Instructions"** field
4. Click **"Save"**

**CRITICAL**: The instructions file is specifically formatted for Gemini. Do NOT use SKILL.md in the instructions field—use GEMINI_INSTRUCTIONS.md.

---

### Step 3: Upload Knowledge Base Files

Gemini Gems support file uploads for knowledge base. Upload these 8 files:

1. [reference/sales-methodologies.md](reference/sales-methodologies.md)
2. [reference/drn-vehicle-search.md](reference/drn-vehicle-search.md)
3. [reference/drn-skip-tracing.md](reference/drn-skip-tracing.md)
4. [reference/drn-risk-scoring.md](reference/drn-risk-scoring.md)
5. [reference/drn-loss-alerts.md](reference/drn-loss-alerts.md)
6. [reference/conversation-analysis-framework.md](reference/conversation-analysis-framework.md)
7. [reference/response-templates.md](reference/response-templates.md)
8. [reference/salesforce-agentforce-integration.md](reference/salesforce-agentforce-integration.md)

**How to Upload**:
- In Gemini Gem settings, look for **"Knowledge"** or **"Files"** section
- Click **"Upload files"**
- Select all 8 files from the `reference/` folder
- Wait for upload to complete (should take 30-60 seconds)

**Note**: If Gemini doesn't support file uploads yet, you'll need to copy-paste the contents of each reference file into the instructions field (see "Alternative Setup" below).

---

### Step 4: Configure Gem Settings

**Gem Name**: Sales Leader Coach

**Description** (for your reference):
"World-class sales coaching AI that analyzes conversations, applies elite sales methodologies (MEDDIC, SPIN, Challenger, Gap Selling), maps to DRNsights products, and generates humanized responses for Salesforce AgentForce training."

**Tone**: Professional, Consultative, Data-Driven

**Optional Settings**:
- **Response Length**: Long (we need detailed analysis)
- **Creativity**: Balanced (not too creative, not too rigid)
- **Formality**: Business Professional

---

### Step 5: Test Your Gem

Copy this sample conversation and paste it into your Gem:

```
Date: 2025-10-15
Rep: Test Rep
Prospect: Sample Prospect, VP Collections, Test Credit Union
Stage: Discovery

Transcript:
Rep: Hi, thanks for taking the time today.
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

**Expected Output**:
- Conversation analysis with grade (should be ~B or B-)
- "What You Did Well" section
- "What You Missed" section (should note: didn't quantify ROI, didn't differentiate from LexisNexis, didn't qualify budget)
- Coached response (full script)
- Tactical coaching
- JSON output

If you get this output, your Gem is working correctly! ✅

---

## Alternative Setup (If File Upload Not Supported)

If Gemini doesn't support file uploads for Gems yet, use this workaround:

### Option A: Paste Files Into Instructions

1. Open **GEMINI_INSTRUCTIONS.md**
2. At the bottom of that file, append the contents of all 8 reference files:

```
--- REFERENCE FILE: sales-methodologies.md ---
[Paste full contents of sales-methodologies.md]

--- REFERENCE FILE: drn-vehicle-search.md ---
[Paste full contents of drn-vehicle-search.md]

[Repeat for all 8 files]
```

3. Paste this COMBINED file into Gemini Gem instructions field

**Warning**: This will create a very long instructions field (~250 KB). Gemini should handle it, but test thoroughly.

---

### Option B: Use Gemini Pro API with Files

If you're comfortable with APIs:

1. Create a Gemini Pro API project in Google Cloud
2. Use the `files.upload` API to upload the 8 reference files
3. Reference those files in your Gem configuration
4. See [Google AI Studio documentation](https://ai.google.dev/tutorials/file_api_quickstart)

---

## Gemini-Specific Features to Leverage

### 1. Multimodal Input (If Supported)

If your Gem supports image input, you can:
- Upload screenshots of Salesforce Opportunity records
- Upload photos of whiteboard notes from sales calls
- Upload scanned handwritten notes

The Gem will extract text and analyze the conversation.

### 2. Google Workspace Integration

If you have Google Workspace, you can:
- Upload Google Docs with conversation transcripts
- Upload Google Sheets with batch conversations
- Export output directly to Google Sheets for analysis

### 3. Voice Input (If Supported)

Some Gemini versions support voice input. If yours does:
- Record your sales call
- Use voice input to transcribe and analyze in real-time
- Get coaching feedback immediately after the call

---

## Testing Checklist

After setup, test these scenarios:

### ✅ Test 1: Single Conversation Analysis
- Input: Copy-paste a single conversation
- Expected: Full analysis with grade, coaching, JSON output
- Pass criteria: Output includes all sections (What You Did Well, What You Missed, Coached Response, etc.)

### ✅ Test 2: Batch CSV Analysis
- Input: Upload a CSV with 5-10 conversations
- Expected: Batch insights + individual analyses
- Pass criteria: Common pain points identified, playbook updates generated

### ✅ Test 3: Product Knowledge Accuracy
- Input: "How does Vehicle Search help with charge-offs?"
- Expected: Accurate response citing "billions of LPR detections," "address scoring," specific features
- Pass criteria: Mentions correct product features from reference files

### ✅ Test 4: Sales Methodology Application
- Input: "Which methodology should I use if prospect is Problem Aware and in Discovery stage?"
- Expected: SPIN Selling, Gap Selling, or Challenger Sale with rationale
- Pass criteria: Correct methodology selected, explains why

### ✅ Test 5: Objection Handling
- Input: "Prospect says 'We already use LexisNexis.' What do I say?"
- Expected: Challenger reframe on stale data, differentiate with "realternative data"
- Pass criteria: Uses language from response-templates.md

---

## Common Issues & Troubleshooting

### Issue 1: Gem Doesn't Reference Uploaded Files
**Symptom**: Responses are generic, don't use specific DRNsights features or statistics

**Solution**:
- Verify files uploaded successfully (check Gem settings → Knowledge)
- Try re-uploading files
- As last resort, use "Alternative Setup" (paste files into instructions)

### Issue 2: Responses Are Too Short
**Symptom**: Analysis is superficial, missing sections like "Coached Response" or "Tactical Coaching"

**Solution**:
- In Gem settings, set Response Length to "Long" or "Detailed"
- Add to instructions: "Always provide COMPLETE analysis with all sections: Overview, Strengths, Weaknesses, Coached Response, Tactical Coaching, Next Steps, JSON"

### Issue 3: Responses Are Too Robotic
**Symptom**: Language sounds formal, uses phrases like "As per our previous conversation"

**Solution**:
- Re-emphasize tone guidelines in instructions
- Add examples of good vs. bad tone
- Test with explicit prompt: "Respond in a conversational, human tone using contractions"

### Issue 4: CSV Upload Not Working
**Symptom**: Gem can't parse CSV format

**Solution**:
- Convert CSV to plain text with `--- CONVERSATION X ---` delimiters
- Use copy-paste format instead of CSV upload
- Or export CSV to Google Sheets, upload Google Sheets link

### Issue 5: JSON Output Is Malformed
**Symptom**: JSON has syntax errors, missing brackets, etc.

**Solution**:
- Add to instructions: "Always validate JSON syntax before outputting. Ensure all brackets, braces, and quotes are properly closed."
- Use a JSON validator like jsonlint.com to check output
- Provide feedback to Gem: "The JSON you provided has a syntax error at line X. Please fix and regenerate."

---

## Optimizing for Gemini vs. Claude

### Key Differences

| Feature | Claude (Original SKILL.md) | Gemini Gem (GEMINI_INSTRUCTIONS.md) |
|---------|---------------------------|-------------------------------------|
| **Instruction Format** | Markdown with YAML frontmatter | Plain text instructions |
| **File References** | Assumes file read access | Requires explicit file upload |
| **Tone Control** | Implicit (follows markdown style) | Explicit (stated in instructions) |
| **JSON Output** | Native support | May need explicit formatting instructions |
| **Tool Use** | Native tool calling | Not applicable (Gems don't have tools) |

### Gemini-Specific Optimizations

1. **Be More Explicit**: Gemini benefits from very explicit instructions (e.g., "Always use contractions," "Always quantify ROI")
2. **Use Examples**: Provide good vs. bad examples for tone, structure, etc.
3. **Repeat Key Points**: Critical instructions (like "reference uploaded files") should be repeated
4. **Format Clearly**: Use headers, bullet points, tables for easy parsing
5. **Test Iteratively**: Gemini may interpret instructions differently—test and refine

---

## Advanced: Integrating with Salesforce via Gemini API

If you want to connect your Gem to Salesforce AgentForce programmatically:

### Step 1: Get Gemini API Key
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create an API key
3. Store securely (you'll need this for API calls)

### Step 2: Create API Endpoint
Use Gemini's REST API to send conversations and receive analysis:

```python
import google.generativeai as genai

genai.configure(api_key="YOUR_API_KEY")

model = genai.GenerativeModel('gemini-1.5-pro')

conversation = """
Date: 2025-10-15
Rep: John Smith
Prospect: Jane Doe, VP Collections, ABC Credit Union
[full transcript]
"""

response = model.generate_content(conversation)
print(response.text)
```

### Step 3: Parse JSON Output
Extract the JSON from Gemini's response and send to Salesforce:

```python
import json
import requests

# Extract JSON from response
json_start = response.text.find('```json') + 7
json_end = response.text.find('```', json_start)
json_data = json.loads(response.text[json_start:json_end])

# Send to Salesforce
salesforce_url = "https://your-instance.salesforce.com/services/data/v60.0/sobjects/Conversation_Intelligence__c/"
headers = {
    "Authorization": "Bearer YOUR_SALESFORCE_TOKEN",
    "Content-Type": "application/json"
}
requests.post(salesforce_url, json=json_data, headers=headers)
```

### Step 4: Automate with Google Cloud Functions
Deploy a Cloud Function that triggers on new Salesforce opportunities:
1. Salesforce Flow → Webhook → Google Cloud Function
2. Cloud Function calls Gemini API with conversation data
3. Cloud Function sends analysis back to Salesforce

---

## Usage Tips

### Tip 1: Start Small
- Analyze 1-3 conversations manually first
- Review output quality
- Adjust instructions if needed
- Then scale to batch processing (10-50 conversations)

### Tip 2: Iterate on Instructions
- Gemini learns from your feedback
- If responses aren't what you want, refine instructions
- Add examples of good vs. bad output
- Test after each change

### Tip 3: Use Templates
- Create saved prompts for common scenarios:
  - "Analyze this lost opportunity conversation"
  - "Generate objection handling playbook for LexisNexis"
  - "Create Knowledge Base article for charge-off conversations"

### Tip 4: Leverage Google Workspace
- Store conversation transcripts in Google Docs
- Use Google Sheets for batch CSV analysis
- Share Gem with your team (if supported)

### Tip 5: Track Performance
- Keep a log of Gem accuracy (how often it gets product details right)
- Note which methodologies it applies most effectively
- Refine instructions based on patterns

---

## Next Steps

1. ✅ Complete setup (Steps 1-5 above)
2. ✅ Test with sample conversation
3. ✅ Analyze 5-10 real conversations
4. ✅ Review output quality and iterate on instructions
5. ✅ Set up Salesforce integration (optional)
6. ✅ Train your sales team on how to use the Gem

---

## Support

If you encounter issues:
1. Check [Gemini Help Center](https://support.google.com/gemini/)
2. Review [Google AI Studio Documentation](https://ai.google.dev/)
3. Email: support@chiefaiofficer.com

---

**You're ready to coach your AI agents to world-class performance with Gemini!** 🚀

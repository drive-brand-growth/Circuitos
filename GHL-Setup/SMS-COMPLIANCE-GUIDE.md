# SMS Marketing Compliance Guide
## Legal Requirements for Sending Business SMS (USA)

**CRITICAL:** Violating SMS laws = $500-$1,500 fine PER MESSAGE + potential lawsuits

---

## 🚨 THE LAW: TCPA (Telephone Consumer Protection Act)

### What You MUST Have Before Sending SMS:

**1. EXPRESS WRITTEN CONSENT** (This is non-negotiable)

You need **explicit, documented permission** from the person to send them SMS messages.

**What counts as valid consent:**
- ✅ Checkbox on web form: "I agree to receive SMS messages from [Business Name]"
- ✅ Text-to-join: "Text JOIN to 12345 to receive updates"
- ✅ Verbal consent (if recorded): "Do you consent to receive text messages?" → "Yes"
- ✅ Paper form with signature agreeing to SMS

**What does NOT count:**
- ❌ Pre-checked boxes
- ❌ "By submitting this form you agree..." (too vague)
- ❌ Just having their phone number
- ❌ They gave you their number verbally without explicit SMS consent
- ❌ They called your business (not consent for YOU to text them)

---

## 📋 REQUIRED ELEMENTS OF SMS CONSENT

Your consent language must include:

### 1. **Clear Disclosure**
```
Example:
"By checking this box and providing your phone number, you agree to
receive marketing text messages from [Business Name] at the number
provided, including messages sent by autodialer. Consent is not a
condition of purchase. Message and data rates may apply. Message
frequency varies."
```

### 2. **How to Opt-Out**
```
"Reply STOP to unsubscribe at any time."
```

### 3. **Help Information**
```
"Reply HELP for help."
```

### 4. **Privacy Policy Link** (if applicable)
```
"View our Privacy Policy: [link]"
```

---

## ✅ COMPLIANT SMS CONSENT FLOW

### Option 1: Web Form Consent (Most Common)

**GHL Form Setup:**

```html
<!-- Phone Number Field -->
<input type="tel" name="phone" required>

<!-- REQUIRED: Consent Checkbox (unchecked by default) -->
<input type="checkbox" name="sms_consent" required>
<label>
  I agree to receive marketing text messages from [Business Name] at
  the phone number provided. Consent is not required to make a purchase.
  Message and data rates may apply. Message frequency varies.
  Reply STOP to opt out or HELP for help.
</label>

<!-- Link to Terms -->
<a href="/sms-terms">SMS Terms & Conditions</a>
```

**GHL Workflow - Store Consent:**
```
TRIGGER: Form submitted

ACTION 1: Check if sms_consent checkbox = TRUE
  IF TRUE:
    - Add tag: "SMS Consent - Web Form"
    - Set custom field: sms_consent_date = NOW()
    - Set custom field: sms_consent_method = "Web Form"
    - Set custom field: sms_consent_ip = {{form_ip_address}}
  ELSE:
    - DO NOT add to SMS sequences
    - Add tag: "No SMS Consent"
```

### Option 2: Text-to-Join (Double Opt-In)

**Setup:**
1. Get a dedicated SMS number from GHL
2. Create keyword: "JOIN" or "DEALS" or "WORKOUT" (industry-specific)

**Workflow:**
```
TRIGGER: Contact texts "JOIN" to your number

AUTO-REPLY (Immediate):
"Thanks for joining [Business Name]! You'll now receive exclusive
offers and updates. Reply STOP to opt out anytime or HELP for help.
Msg & data rates may apply."

THEN:
- Add tag: "SMS Consent - Text to Join"
- Set custom field: sms_consent_date = NOW()
- Set custom field: sms_consent_method = "Keyword - JOIN"
- Add to SMS marketing list
```

### Option 3: Verbal Consent (Phone Call)

**If sales rep gets consent on phone:**

```
Sales Rep Script:
"Great! Can I get your cell phone number to send you appointment
reminders and exclusive offers via text? You can opt out anytime
by replying STOP."

[Customer provides number]

"Perfect. Just to confirm - you're agreeing to receive text messages
from us at [read back number]. Is that correct?"

[Customer confirms]

THEN in GHL:
- Add tag: "SMS Consent - Verbal"
- Set custom field: sms_consent_date = NOW()
- Set custom field: sms_consent_method = "Verbal - [Rep Name]"
- Set custom field: sms_consent_notes = "Confirmed on call with [Rep]"
```

**CRITICAL:** Document verbal consent immediately in contact notes!

---

## 🛑 REQUIRED: INITIAL CONFIRMATION MESSAGE

**First SMS after consent must include:**

```
Hi [FirstName]! This is [Business Name]. You're now signed up for
exclusive offers and updates. Expect 2-4 msgs/month. Msg&data rates
may apply. Reply STOP to opt out or HELP for help.
```

**This must be sent BEFORE any marketing messages.**

---

## 📱 EVERY SMS MUST INCLUDE

### 1. **Business Identification**
Your first message and periodically thereafter must identify your business:
```
"Hi from [Business Name]..."
or
"[Business Name] here - ..."
```

### 2. **Opt-Out Instructions** (Frequency varies by state)
- **Federal law:** Include in initial message + available upon request
- **Best practice:** Include in every message or every campaign

```
Examples:
"Reply STOP to opt out"
"Text STOP to unsubscribe"
```

### 3. **HELP Information** (Available on Request)
When someone texts "HELP", auto-reply:
```
"[Business Name]: For help, contact us at [phone] or [email].
Msg&data rates may apply. Reply STOP to opt out."
```

---

## ⚙️ GHL COMPLIANCE SETUP

### Step 1: Enable Auto-Responses

**GHL Settings → Phone Numbers → Your SMS Number → Keywords**

**Keyword: STOP (Required)**
```
Auto-Reply:
"You've been unsubscribed from [Business Name] text messages.
You will no longer receive messages. Reply START to resubscribe."

Action:
- Remove all SMS tags
- Add tag: "SMS Opt-Out"
- Set custom field: sms_consent = FALSE
- Set custom field: sms_opt_out_date = NOW()
- Add to DNC (Do Not Contact) list for SMS
```

**Keyword: HELP (Required)**
```
Auto-Reply:
"[Business Name] - For assistance, call [phone] or email [email].
Msg&data rates may apply. Reply STOP to opt out."
```

**Keyword: START (Optional but Recommended)**
```
Auto-Reply:
"Welcome back to [Business Name] messages! Reply STOP to opt out
anytime or HELP for help."

Action:
- Add tag: "SMS Consent - Resubscribed"
- Set custom field: sms_consent = TRUE
- Remove from DNC list
```

### Step 2: Create Consent-Gated Workflows

**EVERY SMS workflow must check consent first:**

```
TRIGGER: [Your workflow trigger]

ACTION 1: IF/ELSE - Check SMS Consent
  IF custom_field.sms_consent = TRUE
    AND tag does NOT include "SMS Opt-Out"
    AND phone number is mobile (not landline)
  THEN:
    → Continue to send SMS
  ELSE:
    → Exit workflow (DO NOT SEND)
    → Add tag: "Skipped - No SMS Consent"
```

### Step 3: Track Consent Data

**Required Custom Fields in GHL:**
- `sms_consent` (Checkbox) - TRUE/FALSE
- `sms_consent_date` (Date) - When they consented
- `sms_consent_method` (Text) - Web Form / Verbal / Text-to-Join
- `sms_opt_out_date` (Date) - When they opted out (if applicable)
- `sms_consent_ip` (Text) - IP address from form submission (proof)

---

## 🕐 TIMING RESTRICTIONS

### Federal Guidelines (TCPA):
- **Allowed hours:** 8am - 9pm (recipient's local time zone)
- **Prohibited:** Sundays before 10am in some states

### State-Specific (More Restrictive):

**California:**
- No SMS before 9am or after 9pm

**Florida:**
- No SMS before 8am or after 9pm

**Texas:**
- No SMS before 9am or after 9pm on weekdays
- No SMS before noon on Sundays

**Best Practice:** Send between **9am - 8pm in recipient's timezone**

### GHL Implementation:

```
ACTION: Send SMS

Advanced Settings:
- Respect timezone: ✓ Enabled
- Quiet hours: 9pm - 9am (recipient timezone)
- Skip if outside hours: ✓ Yes (reschedule for 9am next day)
```

---

## 📊 CONTENT RESTRICTIONS

### What You CAN Send:
- ✅ Appointment reminders (transactional - less strict)
- ✅ Order confirmations (transactional)
- ✅ Promotional offers (with consent)
- ✅ Event invitations (with consent)
- ✅ Follow-up after in-person interaction (if verbal consent obtained)

### What You CANNOT Send:
- ❌ Unsolicited marketing (no consent)
- ❌ Adult content
- ❌ Gambling/cannabis (high-risk)
- ❌ Misleading/deceptive content
- ❌ Messages to landlines (unless consent for autodialed calls)

### Message Frequency Disclosure:

You must tell people how often you'll text them:

```
Examples:
"Expect 2-4 messages per month"
"You'll receive daily deals"
"We'll text you about appointments and special offers (approx 5 msgs/month)"
```

---

## 🔒 RECORD KEEPING (CRITICAL)

### What to Store:

**For EVERY contact who receives SMS, you must have:**

1. **Proof of Consent**
   - Date and time of consent
   - Method (form submission, text-to-join, verbal)
   - IP address (if web form)
   - Exact consent language they agreed to

2. **Opt-Out History**
   - If they opted out, when and how (STOP keyword, phone call, etc.)

3. **Message History**
   - What you sent and when
   - GHL stores this automatically in contact timeline

**Retention:** Keep records for **4 years minimum** (TCPA statute of limitations)

### GHL Built-In Tracking:

✅ Contact timeline shows all SMS sent
✅ Tag history shows consent/opt-out events
✅ Custom fields store consent metadata

**Export regularly:**
```
GHL → Contacts → Export
Include fields: sms_consent, sms_consent_date, sms_consent_method
Store backups for compliance audits
```

---

## 🎯 HIGH-INTENT GMB WORKFLOW - COMPLIANT VERSION

### Updated Workflow (Legal SMS):

**STEP 1: Check Consent BEFORE Sending**

```
TRIGGER: Contact scored 85+ (GMB directions clicked)

ACTION 1: IF/ELSE - Verify SMS Consent
  IF custom_field.sms_consent = TRUE
    AND tag does NOT include "SMS Opt-Out"
    AND current_time is between 9am-8pm (contact timezone)
  THEN:
    → Continue to ACTION 2 (Send SMS)
  ELSE:
    → Skip SMS, go directly to email
    → Add tag: "Skipped SMS - No Consent"
```

**STEP 2: Send Compliant SMS**

```
SMS Content:
"Hi {{contact.first_name}}! This is {{business.name}}.

Saw you looked up directions to our gym - we're only {{distance_miles}}
miles from you! Free first session if you come by today or tomorrow.

Reply YES for best times to visit.

Reply STOP to opt out. Msg&data rates may apply."

Note: Includes business name ✓
Note: Includes opt-out info ✓
Note: Under 160 characters (single SMS - lower cost) ✓
```

---

## 💰 COST & CARRIER FILTERING

### SMS Costs:
- **Outbound SMS:** $0.01 - $0.04 per message (varies by carrier)
- **GHL pricing:** Included in phone number ($2-5/mo) + per-message fees

### Carrier Filtering (Automatic Spam Protection):

Carriers (AT&T, Verizon, T-Mobile) automatically block messages with:
- ❌ Shortened URLs (bit.ly, tinyurl) → Use full URLs or GHL branded links
- ❌ All caps text → Use sentence case
- ❌ Excessive emojis → Limit to 1-2
- ❌ High complaint rate → Keep under 0.5% (5 per 1000)

**Best practices to avoid carrier blocking:**
- Keep messages under 160 characters (1 SMS segment)
- Use full URLs or branded short domains
- Limit to 1-2 emojis per message
- Don't send same message to >100 people in <1 hour (looks like spam)

---

## ⚖️ STATE-SPECIFIC LAWS

### California (CCPA/CPRA):
- Must allow data deletion requests
- Must disclose data collection in privacy policy
- 30-day grace period to fix violations

### Florida (Florida TCPA):
- Stricter than federal TCPA
- Requires clearer consent language
- Higher penalties ($500-$1,500 per violation)

### Illinois (BIPA):
- Biometric data restrictions (not SMS-specific, but affects data collection)

**Best practice:** Follow the **strictest state law** (usually California or Florida) for all contacts.

---

## 🚨 PENALTIES FOR VIOLATIONS

### TCPA Fines:
- **Per message:** $500 (unintentional) or $1,500 (willful)
- **Class action lawsuits:** Possible if many people affected
- **Carrier blacklisting:** Your number gets blocked permanently

### Real Examples:
- **Papa John's:** $16.5M settlement (sent texts without consent)
- **Dish Network:** $280M fine (largest TCPA penalty ever)
- **Capital One:** $75M settlement (texted customers who opted out)

---

## ✅ COMPLIANCE CHECKLIST

### Before Sending ANY SMS:

- [ ] Contact explicitly consented (checkbox, keyword, or verbal)
- [ ] Consent is documented in GHL custom fields
- [ ] Initial confirmation message sent
- [ ] STOP/HELP keywords configured in GHL
- [ ] Message includes business name
- [ ] Message includes opt-out instructions (or available via STOP)
- [ ] Sending during allowed hours (9am-8pm recipient timezone)
- [ ] Phone number is mobile (not landline - unless autodialer consent)
- [ ] Contact has NOT opted out (check tags/custom fields)
- [ ] Message frequency matches what you disclosed
- [ ] Records stored for 4+ years

---

## 🎓 RECOMMENDED: SMS TERMS & CONDITIONS PAGE

Create a page on your website:

**URL:** `yourdomain.com/sms-terms`

**Content:**
```
SMS TERMS & CONDITIONS

By opting in to receive SMS messages from [Business Name], you agree to
receive marketing text messages at the phone number provided.

CONSENT: Consent is not a condition of purchase. You can opt out at any time.

FREQUENCY: You will receive approximately 2-4 messages per month.

MESSAGE & DATA RATES: Message and data rates may apply.

OPT-OUT: Reply STOP to opt out at any time. You will receive a confirmation
message. After opting out, you will no longer receive messages unless you
re-subscribe by texting START.

HELP: Reply HELP for customer support. Or contact us at [phone] or [email].

CARRIERS: Carriers are not liable for delayed or undelivered messages.

PRIVACY: We will not sell or share your phone number with third parties.
View our Privacy Policy: [link]

QUESTIONS: Contact us at [email] or [phone].
```

Link to this page in your:
- Web forms (near SMS consent checkbox)
- Initial confirmation message
- HELP auto-reply

---

## 🎯 SUMMARY: HOW TO SEND SMS LEGALLY

### The Simple Version:

1. **Get explicit consent** (checkbox, keyword, or verbal)
2. **Document it** (store in GHL custom fields with date/method)
3. **Send confirmation** ("You're signed up! Reply STOP to opt out")
4. **Include opt-out** in messages (or make available via STOP keyword)
5. **Honor STOP immediately** (within seconds, not days)
6. **Respect quiet hours** (9am-8pm recipient timezone)
7. **Keep records** (4+ years minimum)

### The Even Simpler Version:

**ASK FIRST. LET THEM OPT OUT. SEND DURING BUSINESS HOURS.**

---

## 📚 RESOURCES

**Federal Law:**
- TCPA (47 U.S.C. § 227): https://www.fcc.gov/general/telemarketing-and-robocalls
- FCC TCPA Rules: https://www.fcc.gov/tcpa-rules

**Industry Standards:**
- CTIA Messaging Principles: https://www.ctia.org/the-wireless-industry/industry-commitments/messaging-principles-and-best-practices

**State Laws:**
- California TCPA: https://oag.ca.gov/privacy/ccpa
- Florida TCPA: F.S. 501.059

**Compliance Tools:**
- GHL Knowledge Base - SMS Compliance: https://help.gohighlevel.com
- Twilio TCPA Guide: https://www.twilio.com/docs/glossary/what-is-tcpa

---

## ⚠️ DISCLAIMER

**I am not a lawyer.** This guide is for informational purposes only and does
not constitute legal advice. SMS laws vary by state and are subject to change.

**Recommendation:** Consult with a lawyer specializing in telecommunications law
before launching SMS campaigns, especially if:
- Sending >1,000 messages per month
- Operating in multiple states
- Targeting high-risk industries (finance, healthcare, legal)

---

**© 2025 Circuit OS™**
**Stay Compliant. Respect Opt-Outs. Get Consent.**

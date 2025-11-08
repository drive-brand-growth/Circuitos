# CAN-SPAM Compliant Email Footers

## ⚠️ LEGAL REQUIREMENT - U.S. LAW

**CAN-SPAM Act Penalties:** Up to $51,744 per non-compliant email
**Status:** CRITICAL - Add to ALL emails immediately
**Implementation Time:** 1-2 hours

---

## CAN-SPAM Requirements (Must Have in ALL Marketing Emails)

✅ **1. Physical Address** - Your valid postal address (not P.O. Box unless registered)
✅ **2. Unsubscribe Link** - Clear, conspicuous, one-click unsubscribe
✅ **3. Unsubscribe Honored** - Process opt-outs within 10 business days
✅ **4. Accurate "From" Name** - Sender must be identifiable
✅ **5. Accurate Subject Line** - No deceptive subjects
✅ **6. Identify as Ad** - If promotional, must disclose

**Non-compliant = $51,744 fine PER EMAIL**

---

## Footer Template 1: Standard Cold Email (Instantly.ai)

### Use in: All cold email sequences

```html
---

{{business.legal_name}}
{{business.physical_address}}
{{business.city}}, {{business.state}} {{business.zip}}

📧 You're receiving this because you visited our website or viewed our business listing on Google, indicating potential interest in {{business.category}}.

Don't want emails from us? No problem.
[Unsubscribe]({{unsubscribe_link}}) | [Manage Preferences]({{preferences_link}})

This email was sent to {{contact.email}}.
```

**GHL Variable Mapping:**
- `{{business.legal_name}}` → Custom value: "Your Legal Business Name LLC"
- `{{business.physical_address}}` → "123 Main Street, Suite 100"
- `{{business.city}}` → "Austin"
- `{{business.state}}` → "TX"
- `{{business.zip}}` → "78701"
- `{{business.category}}` → "fitness services" / "restaurant dining" / etc.
- `{{contact.email}}` → GHL variable
- `{{unsubscribe_link}}` → Instantly.ai unsubscribe link
- `{{preferences_link}}` → Link to GHL preference center

---

## Footer Template 2: Warm Follow-Up (Post-Reply)

### Use in: Emails after lead has replied

```html
---

Thanks for connecting with us! We're here to help.

{{business.legal_name}}
{{business.physical_address}}
{{business.city}}, {{business.state}} {{business.zip}}
{{business.phone}} | {{business.website}}

Prefer not to receive future updates? [Unsubscribe]({{unsubscribe_link}})
```

**Why different?**
- Less formal (they've engaged)
- Contact info included (they may want to call)
- Still legally compliant

---

## Footer Template 3: Transactional Emails (Appointment Confirmations, etc.)

### Use in: Non-promotional emails (confirmations, receipts, updates)

**Note:** Transactional emails are EXEMPT from CAN-SPAM unsubscribe requirements, but best practice is to include contact info.

```html
---

{{business.legal_name}}
{{business.physical_address}}
{{business.phone}} | {{business.email}}

Questions? Reply to this email or call us at {{business.phone}}.
```

**No unsubscribe needed** for:
- Appointment confirmations
- Receipt/invoice emails
- Account updates
- Customer service responses

---

## Footer Template 4: Review Request Emails

### Use in: AI-generated review request emails

```html
---

{{business.legal_name}}
{{business.physical_address}}
{{business.city}}, {{business.state}} {{business.zip}}

📧 We're reaching out because you're a valued customer.

This is a one-time request for feedback. You won't receive marketing emails unless you opt in.

[Manage Preferences]({{preferences_link}})
```

**Why different?**
- Sets expectation (one-time request)
- Customer relationship (not cold outreach)
- Still includes address + preference link

---

## Footer Template 5: Re-Engagement Campaign (Cold Leads)

### Use in: Reactivation emails to old leads

```html
---

{{business.legal_name}}
{{business.physical_address}}
{{business.city}}, {{business.state}} {{business.zip}}

📧 It's been a while! We noticed you showed interest in {{business.category}} back in {{first_contact_date}}.

Not interested anymore? [Unsubscribe here]({{unsubscribe_link}}) and we won't bother you again.

Want to hear from us occasionally? [Keep me on the list]({{keep_subscribed_link}})
```

**Best practice:**
- Acknowledge the gap in communication
- Make unsubscribe easy and guilt-free
- Offer "keep me subscribed" option (re-engagement)

---

## Footer Template 6: A/B Test Variants

### Use in: Email Campaign Manager A/B/C testing

**Variant A - Formal**
```html
---
{{business.legal_name}} | {{business.physical_address}} | {{business.city}}, {{business.state}} {{business.zip}}
[Unsubscribe]({{unsubscribe_link}}) | [Privacy Policy]({{privacy_policy_link}})
```

**Variant B - Friendly**
```html
---
Thanks for reading! 👋

{{business.legal_name}}
{{business.physical_address}}, {{business.city}}, {{business.state}} {{business.zip}}

Don't want these emails? [Click here to unsubscribe]({{unsubscribe_link}})
```

**Variant C - Minimal**
```html
---
{{business.legal_name}} · {{business.physical_address}} · {{business.city}}, {{business.state}} {{business.zip}}
[Unsubscribe]({{unsubscribe_link}})
```

**Test which footer drives best engagement** while remaining compliant.

---

## GHL Workflow: Process Unsubscribe (CAN-SPAM Compliance)

### Workflow Name: "CAN-SPAM - Process Unsubscribe"

**Trigger:** Link clicked in email → `{{unsubscribe_link}}`

**Step 1: Update Contact (Immediately)**
```
Update Contact:
   - email_opt_out = TRUE
   - unsubscribe_date = Today
   - unsubscribe_source = "Email Unsubscribe Link"
   - Add Tag: "Unsubscribed - {{today}}"
```

**Step 2: Remove from ALL Email Campaigns**
```
Stop all workflows containing email steps for this contact

API Call to Instantly.ai:
POST https://api.instantly.ai/api/v1/leads/unsubscribe
Body: {
   "email": "{{contact.email}}",
   "campaign_id": "all"
}
```

**Step 3: Add to Suppression List**
```
Add contact.email to:
1. GHL global suppression list
2. Instantly.ai suppression list (via API)
3. Supabase suppression table (for all businesses)

This ensures they NEVER receive marketing emails again, even if re-imported.
```

**Step 4: Send Confirmation (Required by CAN-SPAM)**
```
Send Email (transactional, NOT marketing):
Subject: You've been unsubscribed - {{business.name}}

Body:
Hi {{contact.first_name}},

You've been successfully removed from our email list. You won't receive any more marketing emails from {{business.name}}.

Unsubscribed on: {{today}}
Email: {{contact.email}}

If this was a mistake, you can re-subscribe here: [Re-subscribe Link]

You may still receive:
✅ Transactional emails (receipts, confirmations) if you're a customer
✅ Direct replies to your inquiries

Have a question? Reply to this email or call us at {{business.phone}}.

Regards,
{{business.name}} Team

---
{{business.legal_name}}
{{business.physical_address}}
{{business.city}}, {{business.state}} {{business.zip}}
```

**Step 5: Log Unsubscribe (Compliance Audit Trail)**
```
INSERT INTO unsubscribe_log (
   contact_id,
   email,
   unsubscribe_date,
   unsubscribe_source,
   ip_address,
   user_agent
) VALUES (
   '{{contact.id}}',
   '{{contact.email}}',
   NOW(),
   'Email Link Click',
   '{{ip_address}}',
   '{{user_agent}}'
);
```

**Timeline:** Must complete within 10 business days (CAN-SPAM requirement)
**Best practice:** Complete immediately (within seconds)

---

## GHL Workflow: Manage Email Preferences

### Workflow Name: "Email Preference Center"

**Trigger:** Link clicked → `{{preferences_link}}`

**Step 1: Show Preference Form**
```
GHL Form: "Email Preferences"

Options:
[ ] All emails (promotions, news, updates)
[ ] Important updates only (no promotions)
[ ] Event invitations only
[ ] Unsubscribe from all emails

Frequency:
( ) Daily
( ) Weekly
( ) Monthly
( ) Never

[Save Preferences]
```

**Step 2: Update Contact Based on Selection**
```
IF: "All emails" selected
   - email_opt_out = FALSE
   - email_frequency = "Daily" / "Weekly" / "Monthly"
   - Add Tag: "Email - All Content"

IF: "Important updates only"
   - email_opt_out = FALSE
   - email_frequency = "Monthly"
   - Add Tag: "Email - Updates Only"
   - Remove from promotional campaigns

IF: "Event invitations only"
   - email_opt_out = FALSE
   - Add Tag: "Email - Events Only"
   - Remove from all campaigns except event invitations

IF: "Unsubscribe from all"
   - Trigger: "CAN-SPAM - Process Unsubscribe" workflow
```

**Step 3: Confirm Preferences**
```
Send Email:
Subject: Email preferences updated - {{business.name}}

Body:
Hi {{contact.first_name}},

Your email preferences have been updated:

✅ Subscription: {{selected_option}}
✅ Frequency: {{selected_frequency}}
✅ Updated: {{today}}

Change your mind? Update preferences anytime: [Preferences Link]

Regards,
{{business.name}}
```

---

## Supabase Table: Unsubscribe Log

### Create Compliance Tracking Table

```sql
-- CAN-SPAM Unsubscribe Tracking
CREATE TABLE unsubscribe_log (
   id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
   contact_id VARCHAR(255),
   email VARCHAR(255) NOT NULL,
   unsubscribe_date TIMESTAMP DEFAULT NOW(),
   unsubscribe_source VARCHAR(100), -- 'Email Link', 'Preference Center', 'Manual Request', 'GDPR Deletion'
   ip_address VARCHAR(50),
   user_agent TEXT,
   resubscribe_date TIMESTAMP, -- If they opt back in
   created_at TIMESTAMP DEFAULT NOW()
);

-- Suppression List (Never Email Again)
CREATE TABLE email_suppression_list (
   id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
   email VARCHAR(255) UNIQUE NOT NULL,
   reason VARCHAR(100), -- 'Unsubscribed', 'Hard Bounce', 'Spam Complaint', 'GDPR Deletion'
   suppression_date TIMESTAMP DEFAULT NOW(),
   source VARCHAR(100), -- 'GHL', 'Instantly.ai', 'Manual'
   notes TEXT,
   created_at TIMESTAMP DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_unsubscribe_email ON unsubscribe_log(email);
CREATE INDEX idx_unsubscribe_date ON unsubscribe_log(unsubscribe_date);
CREATE INDEX idx_suppression_email ON email_suppression_list(email);
```

---

## Implementation Checklist

### Day 1: Update Email Templates

- [ ] Add CAN-SPAM footer to all Instantly.ai cold email templates
- [ ] Add CAN-SPAM footer to all GHL email workflows
- [ ] Add CAN-SPAM footer to all Email Campaign Manager templates (A/B/C variants)
- [ ] Update review request email templates
- [ ] Update re-engagement email templates

### Day 2: Build Workflows

- [ ] Create "CAN-SPAM - Process Unsubscribe" workflow
- [ ] Create "Email Preference Center" workflow
- [ ] Test unsubscribe flow (10 test contacts)
- [ ] Create public preference center form

### Day 3: Suppression List Integration

- [ ] Create Supabase suppression tables (SQL above)
- [ ] Sync existing GHL unsubscribed contacts to suppression list
- [ ] Configure Instantly.ai suppression list sync
- [ ] Build API endpoint to check suppression before sending

### Day 4: Audit & Training

- [ ] Audit all existing email templates for compliance
- [ ] Train staff on CAN-SPAM requirements
- [ ] Document unsubscribe SLA (within 10 days)
- [ ] Set up monthly compliance report

---

## Business Information Variables (Update These)

### Required for ALL Email Footers

**In GHL Custom Values, add:**

```
business.legal_name = "Your Legal Business Name LLC"
business.physical_address = "123 Main Street, Suite 100"
business.city = "Austin"
business.state = "TX"
business.zip = "78701"
business.phone = "(555) 123-4567"
business.email = "info@yourbusiness.com"
business.website = "https://yourbusiness.com"
business.category = "fitness services" / "restaurant dining" / etc.
```

**Update location:**
GHL Settings → Custom Values → Add these variables

**Use in emails:**
All email templates can now use `{{business.legal_name}}` etc.

---

## CAN-SPAM vs GDPR Comparison

| Requirement | CAN-SPAM (USA) | GDPR (EU) |
|-------------|----------------|-----------|
| **Opt-out required** | ✅ Yes (after first email) | ✅ Yes (before first email) |
| **Physical address** | ✅ Required in footer | ❌ Not required |
| **Opt-out deadline** | 10 business days | Immediately |
| **Consent required** | ❌ No (opt-out model) | ✅ Yes (opt-in model) |
| **Penalty** | $51,744 per email | €20M or 4% revenue |

**If you have EU customers:** Must comply with BOTH (use stricter GDPR rules)

---

## Common CAN-SPAM Violations (Avoid These)

❌ **No physical address** - Most common violation
❌ **Deceptive subject lines** - "RE: Your order" when there's no order
❌ **No unsubscribe link** - Or link is broken/hidden
❌ **Slow opt-out processing** - Taking >10 days to remove from list
❌ **Ignoring unsubscribes** - Continuing to email after opt-out
❌ **Fake "From" name** - Sender not identifiable

**Result:** $51,744 fine per violation × number of emails sent

---

## Testing Your Compliance

### Test 1: Send Test Email
```
Send email to yourself → Check footer has:
✅ Business legal name
✅ Full physical address
✅ Working unsubscribe link
✅ Clear sender identification
```

### Test 2: Test Unsubscribe Flow
```
Click unsubscribe link → Check:
✅ Immediately removed from campaigns
✅ Confirmation email received
✅ Added to suppression list
✅ No more emails received
```

### Test 3: Audit All Templates
```
Review all email templates → Ensure:
✅ All have compliant footer
✅ Subject lines are accurate
✅ "From" name is identifiable
✅ No deceptive content
```

---

## Monthly Compliance Report (Automated)

### GHL Report: "CAN-SPAM Compliance Dashboard"

**Metrics to track:**
- Total emails sent this month: {{count}}
- Unsubscribe rate: {{unsubscribes / emails_sent}}%
- Avg time to process unsubscribe: {{avg_hours}} hours
- Suppression list size: {{count suppression_list}}
- Bounce rate: {{bounces / emails_sent}}%
- Spam complaints: {{spam_reports}}

**Red flags:**
- ⚠️ Unsubscribe rate >2% (industry avg is 0.1-0.5%)
- ⚠️ Spam complaint rate >0.1%
- ⚠️ Bounce rate >2%
- 🚨 Any unsubscribe processed >10 days

**Action:** If red flags appear, audit email quality and compliance.

---

## Support Resources

**CAN-SPAM Act Official Guide:**
https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business

**Report Spam Violations:**
FTC Complaint Assistant: https://www.ftccomplaintassistant.gov/

**Legal Counsel:**
Consult attorney for jurisdiction-specific requirements (especially if you email EU/CA residents)

---

**IMPLEMENTATION DEADLINE:** Add compliant footers to ALL emails within 48 hours to avoid fines.

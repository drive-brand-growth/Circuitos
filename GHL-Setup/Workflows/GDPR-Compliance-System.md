# GDPR Compliance System for CircuitOS

## ⚠️ LEGAL REQUIREMENT - MUST IMPLEMENT

**EU GDPR Fines:** Up to €20 million or 4% of annual revenue (whichever is higher)
**Status:** CRITICAL - Implement immediately
**Implementation Time:** 4-6 hours

---

## Overview

This system ensures CircuitOS complies with all GDPR requirements:
- ✅ Right to Access (Article 15)
- ✅ Right to Rectification (Article 16)
- ✅ Right to Erasure/"Right to be Forgotten" (Article 17)
- ✅ Right to Data Portability (Article 20)
- ✅ Right to Object (Article 21)
- ✅ Consent tracking and management
- ✅ Data retention policies
- ✅ Breach notification procedures

---

## Part 1: GHL Custom Fields (Consent & Compliance Tracking)

### Add These Custom Fields to GHL Contacts

```
Contact Custom Fields (Compliance):

1. gdpr_consent_date: Date
   - When they gave consent to be contacted

2. gdpr_consent_method: Dropdown
   - Options: "Website Form", "Email Opt-In", "Phone Verbal", "In-Person", "Imported Database", "Virtual LPR Detection"

3. gdpr_consent_status: Dropdown
   - Options: "Active", "Withdrawn", "Pending Verification"

4. gdpr_data_subject_request: Dropdown
   - Options: "None", "Access Requested", "Deletion Requested", "Rectification Requested", "Portability Requested"

5. gdpr_request_date: Date
   - When data subject request was made

6. gdpr_request_fulfilled_date: Date
   - When request was completed

7. data_retention_category: Dropdown
   - Options: "Active Lead", "Converted Customer", "Archive (90 days)", "Archive (2 years)", "Delete After Fulfillment"

8. gdpr_deletion_scheduled: Date
   - Auto-delete date (null if keeping)

9. legitimate_interest_basis: Text Area
   - Document why you can contact without explicit consent (e.g., "Visited website 3 times, expressed interest in membership")

10. data_processing_consent: Boolean
   - Specific consent for AI processing/enrichment
```

---

## Part 2: GHL Workflow - GDPR Data Access Request

**File:** Import this into GHL Workflows

### Workflow: "GDPR - Data Access Request"

**Trigger:** Form submission "GDPR Request Form" OR Email sent to `gdpr@yourdomain.com`

**Step 1: Verify Identity**
```
IF: Form submission
   - Capture: email, phone, full_name
   - Send SMS verification code to phone
   - Wait for code verification (30 min timeout)

IF: Email request
   - Reply: "Please verify your identity at [GDPR Request Form Link]"
   - Wait for form submission
```

**Step 2: Update Contact Record**
```
Update Contact:
   - gdpr_data_subject_request = "Access Requested"
   - gdpr_request_date = Today
   - Add Tag: "GDPR Request - Pending"
```

**Step 3: Generate Data Export (API Call to Vercel Function)**
```
POST to: https://your-vercel.com/api/gdpr-export
Body:
{
   "contact_id": "{{contact.id}}",
   "email": "{{contact.email}}",
   "request_type": "access"
}

This function will:
1. Query GHL API for all contact data
2. Query Supabase for conversation history, ML data
3. Query Instantly.ai for email campaign history
4. Compile into PDF report
5. Upload to GHL Files
6. Return download URL
```

**Step 4: Email Data Export**
```
Send Email:
Subject: Your Data Export from [Business Name]

Body:
Hi {{contact.first_name}},

Per your GDPR data access request on {{gdpr_request_date}}, attached is a complete export of all personal data we hold about you.

This export includes:
✅ Contact information (name, email, phone, address)
✅ All custom fields and enrichment data (200+ attributes)
✅ Email communication history
✅ SMS communication history
✅ Website visit history
✅ AI interaction logs
✅ Lead scoring data
✅ Campaign engagement history

You have the right to:
- Request corrections to inaccurate data
- Request deletion of your data
- Object to processing
- Export this data to another provider

To exercise these rights, reply to this email or visit: [GDPR Portal Link]

Regards,
[Business Name] Data Protection Team
---
Attachment: [PDF Export Link]
```

**Step 5: Update Compliance Record**
```
Update Contact:
   - gdpr_request_fulfilled_date = Today
   - Remove Tag: "GDPR Request - Pending"
   - Add Tag: "GDPR Request - Fulfilled"

Create Task for Owner:
   - Title: "GDPR Access Request Fulfilled - {{contact.email}}"
   - Due: Today
   - Note: "Data export sent. Monitor for follow-up requests (deletion, rectification)."
```

**Step 6: Log Compliance Event**
```
API Call to Supabase:
INSERT INTO gdpr_compliance_log (
   contact_id,
   request_type,
   request_date,
   fulfilled_date,
   action_taken,
   staff_member
) VALUES (
   '{{contact.id}}',
   'access',
   '{{gdpr_request_date}}',
   '{{gdpr_request_fulfilled_date}}',
   'Data export sent via email',
   '{{workflow.executed_by}}'
);
```

---

## Part 3: GHL Workflow - GDPR Deletion Request ("Right to be Forgotten")

### Workflow: "GDPR - Deletion Request"

**Trigger:** Form submission "Delete My Data" OR Email to `gdpr@yourdomain.com` with subject containing "delete" or "forget"

**Step 1: Verify Identity** (same as Access Request)

**Step 2: Check for Legal Obligations**
```
IF: Contact has active deal OR converted customer with purchase <7 years ago
   - Send Email: "We must retain certain data for tax/legal purposes (7 years). We can anonymize your data instead. Proceed?"
   - Wait for confirmation

IF: Contact has no legal retention requirement
   - Proceed to deletion
```

**Step 3: Delete from External Systems (API Calls)**

```javascript
// Call 1: Remove from Instantly.ai
POST to: https://your-vercel.com/api/instantly-delete
Body: {
   "email": "{{contact.email}}",
   "action": "unsubscribe_and_delete"
}

// Call 2: Delete from Supabase
POST to: https://your-vercel.com/api/supabase-delete
Body: {
   "contact_id": "{{contact.id}}",
   "tables": ["conversations", "email_ab_tests", "api_usage_tracking", "gdpr_compliance_log"]
}

// Call 3: Delete from ML training data
POST to: https://your-vercel.com/api/ml-data-delete
Body: {
   "contact_id": "{{contact.id}}",
   "anonymize": false  // true = keep for training but remove PII, false = full delete
}
```

**Step 4: Delete from GHL CRM**
```
Update Contact (before deletion):
   - email = "deleted_{{contact.id}}@gdpr-compliant.local"
   - phone = NULL
   - first_name = "DELETED"
   - last_name = "GDPR"
   - address = NULL
   - Clear all custom fields
   - Add Tag: "GDPR Deleted - {{today}}"

Wait 24 hours (allows for backup/audit)

Then:
   - Delete Contact from GHL CRM
```

**Step 5: Send Confirmation Email (BEFORE deletion)**
```
Send Email to: {{original_email}}
Subject: Your Data Has Been Deleted

Body:
Hi {{contact.first_name}},

Per your request on {{gdpr_request_date}}, all your personal data has been deleted from our systems.

What we deleted:
✅ Contact information (email, phone, address)
✅ All enrichment data (200+ attributes)
✅ Email/SMS communication history
✅ Website visit history
✅ AI interaction logs
✅ Lead scoring data
✅ Campaign engagement data

Your data was removed from:
✅ GoHighLevel CRM
✅ Instantly.ai email platform
✅ Supabase database
✅ AI/ML training datasets

You will not receive any further marketing communications from us.

If you change your mind or need to contact us again, you may do so, but it will be treated as a new inquiry.

Regards,
[Business Name] Data Protection Team
```

**Step 6: Log Deletion**
```
INSERT INTO gdpr_compliance_log (
   contact_id,
   original_email,
   request_type,
   request_date,
   fulfilled_date,
   action_taken,
   data_deleted
) VALUES (
   '{{contact.id}}',
   '{{contact.email}}',
   'deletion',
   '{{gdpr_request_date}}',
   '{{today}}',
   'Full deletion across all systems',
   '{
      "ghl": true,
      "instantly": true,
      "supabase": true,
      "ml_training": true
   }'
);
```

---

## Part 4: Automated Data Retention & Deletion

### Workflow: "Auto-Delete Old Leads (GDPR Retention Policy)"

**Trigger:** Scheduled - Daily at 3:00 AM

**Step 1: Find Contacts Eligible for Deletion**
```
Search GHL Contacts WHERE:
   - last_activity_date < 2 years ago
   - AND converted = false (never became customer)
   - AND data_retention_category = "Archive (2 years)"
   - AND gdpr_deletion_scheduled = Today
```

**Step 2: For Each Contact Found**
```
Send final notice (30 days before deletion):
   - "We haven't heard from you in 2 years. Your data will be deleted in 30 days unless you opt to stay in touch."
   - Link: "Keep My Data" (extends retention to +1 year)

IF: No response after 30 days
   - Execute deletion workflow (same as GDPR Deletion Request)

IF: "Keep My Data" clicked
   - Update data_retention_category = "Active Lead"
   - Clear gdpr_deletion_scheduled
   - Add Tag: "Re-engaged"
```

**Step 3: Anonymize Converted Customers (7+ Years Old)**
```
Search GHL Contacts WHERE:
   - converted = true
   - conversion_date < 7 years ago
   - AND data_retention_category = "Converted Customer"

For Each:
   - Keep: first_name, revenue data, conversion metrics (for reporting)
   - Anonymize: email → "customer_{{id}}@anonymized.local"
   - Delete: phone, address, all PII custom fields
   - Add Tag: "Anonymized - {{today}}"
```

---

## Part 5: Consent Tracking System

### Workflow: "Track GDPR Consent (Virtual LPR Leads)"

**Trigger:** Contact created via Virtual LPR

**Step 1: Determine Consent Basis**
```
IF: Source = "Website Form Submission"
   - gdpr_consent_method = "Website Form"
   - gdpr_consent_status = "Active"
   - gdpr_consent_date = Today

IF: Source = "Virtual LPR Detection" (passive detection)
   - gdpr_consent_method = "Virtual LPR Detection"
   - gdpr_consent_status = "Pending Verification"
   - legitimate_interest_basis = "User visited website {{visit_count}} times, viewed {{pages_viewed}} pages, indicating commercial interest per GDPR Article 6(1)(f)"

IF: Source = "Imported Database"
   - gdpr_consent_method = "Imported Database"
   - gdpr_consent_status = "Pending Verification"
   - Send email: "Confirm you want to hear from us" (double opt-in)
```

**Step 2: Document Legitimate Interest (for Virtual LPR)**
```
Update Contact:
   - legitimate_interest_basis = "
      Lead detected via Virtual LPR on {{detection_date}}.

      Legitimate Interest Basis (GDPR Article 6(1)(f)):
      - User visited website {{visit_count}} times
      - Viewed business listing on Google {{gmb_view_count}} times
      - Searched for keywords: {{search_keywords}}
      - Located within service area ({{distance_miles}} miles)
      - Demonstrated commercial interest in {{business_category}}

      Balancing Test:
      - Our interest: Connect potential customers with local businesses
      - User's interest: Receive relevant local offers
      - No high-risk processing (no sensitive data)
      - User can opt-out at any time

      Legitimate interest assessment documented {{today}}.
   "
```

**Step 3: First Email Must Include GDPR Notice**
```
In ALL first emails, include footer:

---
📧 You're receiving this because you [visited our website/viewed our listing/expressed interest in our services].

You have the right to:
✅ Access your data: [Link to GDPR Portal]
✅ Correct inaccurate data
✅ Request deletion
✅ Object to processing
✅ Unsubscribe: [One-Click Unsubscribe]

We process your data under legitimate interest (GDPR Article 6(1)(f)). Read our privacy policy: [Link]
```

---

## Part 6: Breach Notification System

### Workflow: "GDPR Data Breach Response"

**Trigger:** Manual - Created by staff if breach detected

**Step 1: Assess Breach Severity**
```
Form Fields:
- What data was breached? (Checkboxes: Email, Phone, Address, Payment Info, Health Data, etc.)
- How many contacts affected?
- Was data encrypted?
- Was breach contained?
- Potential harm to individuals: (Low/Medium/High)
```

**Step 2: Automatic Severity Calculation**
```
IF: Payment info OR Health data OR High harm
   - Severity = "CRITICAL - Report to ICO within 72 hours"
   - Create Task: "Report to ICO" (Due: 72 hours from now)
   - Create Task: "Notify affected individuals" (Due: 24 hours)

IF: Email/phone only AND Low harm AND encrypted
   - Severity = "LOW - Document internally, may not require reporting"
```

**Step 3: Notify Data Protection Authority (if required)**
```
Email Template to ICO (UK) or relevant EU authority:

Subject: Data Breach Notification - [Business Name]

Per GDPR Article 33, we are notifying you of a personal data breach:

Breach Details:
- Date/time discovered: {{breach_date}}
- Data affected: {{data_types}}
- Number of individuals: {{contact_count}}
- Cause: {{breach_cause}}
- Containment measures: {{containment}}

Risk Assessment:
- Potential harm: {{harm_level}}
- Mitigating factors: {{mitigations}}

Actions Taken:
- {{action_1}}
- {{action_2}}

Contact: [DPO Name], [Email], [Phone]
```

**Step 4: Notify Affected Individuals**
```
IF: Breach severity = High
   - Send personalized email to each affected contact

Email Template:

Subject: Important Security Notice - [Business Name]

Hi {{contact.first_name}},

We are writing to inform you of a data security incident that may affect your personal information.

What Happened:
{{breach_description}}

What Data Was Affected:
{{data_types}} - Your [email/phone/etc.]

What We're Doing:
✅ {{action_1}}
✅ {{action_2}}
✅ Strengthened security measures

What You Should Do:
- Monitor your accounts for suspicious activity
- {{recommended_action}}

We sincerely apologize for this incident. Your trust is paramount to us.

Questions? Contact our Data Protection Officer: gdpr@yourdomain.com

Regards,
[Business Name] Security Team
```

**Step 5: Document Breach**
```
INSERT INTO gdpr_breach_log (
   breach_date,
   discovery_date,
   data_types_affected,
   contact_count,
   severity,
   reported_to_authority,
   individuals_notified,
   containment_measures,
   lessons_learned
) VALUES (...);
```

---

## Part 7: Supabase Database Schema

### Create Compliance Tracking Tables

```sql
-- Table 1: GDPR Compliance Log
CREATE TABLE gdpr_compliance_log (
   id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
   contact_id VARCHAR(255),
   original_email VARCHAR(255),
   request_type VARCHAR(50), -- 'access', 'deletion', 'rectification', 'portability', 'objection'
   request_date TIMESTAMP,
   fulfilled_date TIMESTAMP,
   action_taken TEXT,
   data_deleted JSONB,
   staff_member VARCHAR(255),
   created_at TIMESTAMP DEFAULT NOW()
);

-- Table 2: GDPR Breach Log
CREATE TABLE gdpr_breach_log (
   id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
   breach_date TIMESTAMP,
   discovery_date TIMESTAMP,
   data_types_affected TEXT[],
   contact_count INT,
   severity VARCHAR(20), -- 'LOW', 'MEDIUM', 'HIGH', 'CRITICAL'
   breach_cause TEXT,
   containment_measures TEXT,
   reported_to_authority BOOLEAN DEFAULT false,
   authority_name VARCHAR(255),
   report_date TIMESTAMP,
   individuals_notified BOOLEAN DEFAULT false,
   notification_date TIMESTAMP,
   lessons_learned TEXT,
   created_at TIMESTAMP DEFAULT NOW()
);

-- Table 3: Consent Audit Trail
CREATE TABLE consent_audit_trail (
   id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
   contact_id VARCHAR(255),
   email VARCHAR(255),
   consent_action VARCHAR(50), -- 'given', 'withdrawn', 'updated'
   consent_method VARCHAR(100), -- 'website_form', 'email_optin', 'virtual_lpr', etc.
   consent_status VARCHAR(50), -- 'active', 'withdrawn', 'pending'
   legitimate_interest_basis TEXT,
   ip_address VARCHAR(50),
   user_agent TEXT,
   timestamp TIMESTAMP DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX idx_compliance_log_contact ON gdpr_compliance_log(contact_id);
CREATE INDEX idx_compliance_log_date ON gdpr_compliance_log(request_date);
CREATE INDEX idx_breach_log_severity ON gdpr_breach_log(severity);
CREATE INDEX idx_consent_trail_contact ON consent_audit_trail(contact_id);
```

---

## Part 8: Vercel API Functions

### File: `/api/gdpr-export.js`

```javascript
// GDPR Data Export Function
import Anthropic from "@anthropic-ai/sdk";
import { createClient } from "@supabase/supabase-js";
import PDFDocument from "pdfkit";

const supabase = createClient(
  process.env.SUPABASE_URL,
  process.env.SUPABASE_KEY
);

export default async function handler(req, res) {
  if (req.method !== "POST") {
    return res.status(405).json({ error: "Method not allowed" });
  }

  const { contact_id, email, request_type } = req.body;

  try {
    // 1. Fetch data from GHL API
    const ghlData = await fetchGHLContactData(contact_id);

    // 2. Fetch data from Supabase
    const { data: conversations } = await supabase
      .from("conversations")
      .select("*")
      .eq("lead_id", contact_id);

    const { data: emailTests } = await supabase
      .from("email_ab_tests")
      .select("*")
      .eq("contact_email", email);

    // 3. Fetch data from Instantly.ai (if applicable)
    const instantlyData = await fetchInstantlyData(email);

    // 4. Compile into structured JSON
    const exportData = {
      personal_information: {
        first_name: ghlData.firstName,
        last_name: ghlData.lastName,
        email: ghlData.email,
        phone: ghlData.phone,
        address: ghlData.address,
        created_date: ghlData.dateAdded,
        source: ghlData.source,
      },
      enrichment_data: ghlData.customFields,
      communication_history: {
        emails_sent: instantlyData?.emails || [],
        sms_sent: ghlData.smsHistory || [],
        calls: ghlData.callHistory || [],
      },
      ai_interactions: conversations,
      campaign_data: emailTests,
      lead_scoring: {
        lpr_score: ghlData.customFields.lprScore,
        fit_score: ghlData.customFields.fitScore,
        intent_score: ghlData.customFields.intentScore,
        timing_score: ghlData.customFields.timingScore,
      },
      consent_records: {
        consent_date: ghlData.customFields.gdpr_consent_date,
        consent_method: ghlData.customFields.gdpr_consent_method,
        consent_status: ghlData.customFields.gdpr_consent_status,
      },
    };

    // 5. Generate PDF report
    const pdfBuffer = await generateGDPRPDF(exportData, email);

    // 6. Upload to GHL or return as download
    res.setHeader("Content-Type", "application/pdf");
    res.setHeader(
      "Content-Disposition",
      `attachment; filename="gdpr-export-${email}-${Date.now()}.pdf"`
    );
    res.send(pdfBuffer);

    // 7. Log compliance action
    await supabase.from("gdpr_compliance_log").insert({
      contact_id,
      original_email: email,
      request_type: "access",
      request_date: new Date(),
      fulfilled_date: new Date(),
      action_taken: "Data export generated and sent",
      staff_member: "Automated System",
    });
  } catch (error) {
    console.error("GDPR export error:", error);
    res.status(500).json({ error: "Failed to generate export" });
  }
}

async function fetchGHLContactData(contactId) {
  // Call GHL API to get contact data
  const response = await fetch(
    `https://rest.gohighlevel.com/v1/contacts/${contactId}`,
    {
      headers: {
        Authorization: `Bearer ${process.env.GHL_API_KEY}`,
      },
    }
  );
  return response.json();
}

async function fetchInstantlyData(email) {
  // Call Instantly.ai API to get campaign data
  const response = await fetch(
    `https://api.instantly.ai/api/v1/leads/${email}`,
    {
      headers: {
        Authorization: `Bearer ${process.env.INSTANTLY_API_KEY}`,
      },
    }
  );
  return response.json();
}

async function generateGDPRPDF(data, email) {
  const doc = new PDFDocument();
  const chunks = [];

  doc.on("data", (chunk) => chunks.push(chunk));
  doc.on("end", () => {});

  // Header
  doc.fontSize(20).text("GDPR Data Export", { align: "center" });
  doc.fontSize(12).text(`Email: ${email}`, { align: "center" });
  doc.fontSize(10).text(`Generated: ${new Date().toISOString()}`, {
    align: "center",
  });
  doc.moveDown();

  // Personal Information
  doc.fontSize(16).text("Personal Information");
  doc.fontSize(10);
  Object.entries(data.personal_information).forEach(([key, value]) => {
    doc.text(`${key}: ${value}`);
  });
  doc.moveDown();

  // Enrichment Data
  doc.fontSize(16).text("Enrichment Data (200+ Attributes)");
  doc.fontSize(10);
  Object.entries(data.enrichment_data).forEach(([key, value]) => {
    doc.text(`${key}: ${value}`);
  });
  doc.moveDown();

  // Communication History
  doc.fontSize(16).text("Communication History");
  doc.fontSize(10);
  doc.text(`Emails sent: ${data.communication_history.emails_sent.length}`);
  doc.text(`SMS sent: ${data.communication_history.sms_sent.length}`);
  doc.moveDown();

  // Lead Scoring
  doc.fontSize(16).text("Lead Scoring Data");
  doc.fontSize(10);
  Object.entries(data.lead_scoring).forEach(([key, value]) => {
    doc.text(`${key}: ${value}`);
  });

  doc.end();

  return Buffer.concat(chunks);
}
```

---

## Part 9: GHL GDPR Request Form

### Create Public Form in GHL

**Form Name:** "GDPR Data Request"
**URL:** `https://yourdomain.com/gdpr-request`

**Fields:**
1. Full Name (required)
2. Email Address (required)
3. Phone Number (required)
4. Request Type (dropdown):
   - Access my data
   - Delete my data
   - Correct my data
   - Export my data
   - Object to processing
5. Additional Details (text area)
6. Verification Code (SMS verification)

**Submit Action:**
- Trigger Workflow: "GDPR - Data Access Request" OR "GDPR - Deletion Request"

---

## Part 10: Privacy Policy Template

### Required Legal Document

```markdown
# Privacy Policy - [Business Name]

Last Updated: [Date]

## 1. Data Controller
[Business Legal Name]
[Address]
Email: gdpr@yourdomain.com
Phone: [Phone]

## 2. What Data We Collect
- Contact information (name, email, phone, address)
- Website activity (pages viewed, time spent, links clicked)
- Google My Business engagement (directions requested, calls made)
- Social media engagement (profile views, link clicks)
- Email/SMS engagement (opens, clicks, replies)
- Enrichment data (location, demographics, business information)

## 3. Legal Basis for Processing
We process your data under:
- **Consent** (GDPR Article 6(1)(a)): When you submit a form or opt-in
- **Legitimate Interest** (GDPR Article 6(1)(f)): When you visit our website or view our listing
- **Contract** (GDPR Article 6(1)(b)): When you become a customer

## 4. How We Use Your Data
- Send marketing communications about our services
- Analyze behavior to personalize offers
- Improve our services through AI/ML analysis
- Respond to inquiries and support requests

## 5. Data Sharing
We share your data with:
- Email service providers (Instantly.ai)
- CRM platform (GoHighLevel)
- AI processing (Anthropic Claude API)
- Analytics (Google Analytics)

We do NOT sell your data to third parties.

## 6. Data Retention
- Active leads: Retained while you engage with us
- Inactive leads: Deleted after 2 years of inactivity
- Customers: Retained for 7 years (tax/legal requirement), then anonymized

## 7. Your Rights (GDPR)
You have the right to:
✅ Access your data
✅ Rectify inaccurate data
✅ Request deletion ("right to be forgotten")
✅ Object to processing
✅ Export your data
✅ Withdraw consent
✅ Lodge a complaint with the ICO

To exercise these rights: gdpr@yourdomain.com or [GDPR Request Form]

## 8. Data Security
We protect your data with:
- Encryption in transit (TLS/SSL)
- Encryption at rest (AES-256)
- Access controls and authentication
- Regular security audits
- Staff training on data protection

## 9. Cookies
We use cookies for:
- Website analytics (Google Analytics)
- Session management
- Marketing tracking

You can disable cookies in your browser settings.

## 10. Changes to This Policy
We may update this policy. Check this page regularly for changes.

## 11. Contact
Questions about your data? Contact:
Data Protection Officer: gdpr@yourdomain.com
[Business Address]
```

---

## Part 11: Implementation Checklist

### Week 1: Foundation

- [ ] Add 10 GDPR custom fields to GHL contacts
- [ ] Create Supabase compliance tables (SQL script above)
- [ ] Deploy Vercel GDPR export function
- [ ] Create public GDPR request form in GHL
- [ ] Publish privacy policy on website

### Week 2: Workflows

- [ ] Build "GDPR - Data Access Request" workflow
- [ ] Build "GDPR - Deletion Request" workflow
- [ ] Build "Track GDPR Consent" workflow (auto-trigger on contact creation)
- [ ] Build "Auto-Delete Old Leads" workflow (scheduled daily)

### Week 3: Training & Testing

- [ ] Train staff on GDPR procedures
- [ ] Test data export function (5 sample contacts)
- [ ] Test deletion workflow (1 test contact)
- [ ] Document breach response plan
- [ ] Assign Data Protection Officer (DPO)

### Week 4: Ongoing Compliance

- [ ] Monthly audit: Review consent records
- [ ] Quarterly audit: Check data retention compliance
- [ ] Annual audit: Full GDPR compliance review
- [ ] Monitor: ICO guidance updates

---

## Part 12: Quick Reference - Response Times

| Request Type | Legal Deadline | Your SLA |
|--------------|----------------|----------|
| Data Access | 30 days | 7 days |
| Data Deletion | 30 days | 7 days |
| Data Rectification | 30 days | 3 days |
| Data Breach Notification (to authority) | 72 hours | 48 hours |
| Data Breach Notification (to individuals) | "Without undue delay" | 24 hours |

---

## Support

Questions about implementation?
- Review: `/Docs/SECURITY-IMPLEMENTATION.md`
- Contact: Your legal counsel for jurisdiction-specific requirements
- Reference: https://gdpr.eu/ (official GDPR text)

---

**CRITICAL:** This is a legal compliance requirement. Implement immediately to avoid fines up to €20M.

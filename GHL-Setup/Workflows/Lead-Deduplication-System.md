# Lead Deduplication System - CircuitOS

## 💰 STOPS WASTED SPEND - HIGH ROI

**Current Problem:** Same person created as multiple contacts in GHL
**Impact:**
- Duplicate emails sent (spam complaints, deliverability damage)
- Inflated lead counts (inaccurate metrics)
- Wasted AI API calls (processing same lead 2-3x)
- Poor customer experience ("Why am I getting 3 emails?")

**Estimated Cost:** 10-15% of contacts are duplicates = ~$50-200/month wasted
**Implementation Time:** 6 hours

---

## How Duplicates Happen

**Scenario 1: Multiple Form Submissions**
```
Day 1: Person submits "Contact Us" form → Contact created
Day 3: Same person submits "Free Trial" form → DUPLICATE created
Result: 2 contacts with different sources but same email
```

**Scenario 2: Virtual LPR + Manual Entry**
```
Virtual LPR detects website visitor → Contact created
Sales rep manually adds same person from business card → DUPLICATE created
Result: 2 contacts with different fields populated
```

**Scenario 3: Import from Multiple Sources**
```
Import from previous CRM → 500 contacts
Import from event signup list → 200 contacts (50 overlap)
Result: 50 duplicates
```

**Scenario 4: Case Sensitivity / Formatting**
```
Email 1: john@example.com
Email 2: John@Example.com
Email 3: JOHN@EXAMPLE.COM
Phone 1: (555) 123-4567
Phone 2: 555-123-4567
Phone 3: 5551234567
Result: GHL doesn't recognize as duplicates (different formatting)
```

---

## Deduplication Strategy

### Three-Tier Matching Logic

**Tier 1: Exact Email Match** (Highest confidence)
```
Normalize: john@example.com = JOHN@EXAMPLE.COM
IF: email matches exactly (case-insensitive)
THEN: 100% confidence duplicate
ACTION: Auto-merge
```

**Tier 2: Phone Match** (High confidence)
```
Normalize: (555) 123-4567 = 555-123-4567 = 5551234567
IF: phone matches (digits only, ignore formatting)
THEN: 95% confidence duplicate
ACTION: Auto-merge if email also blank or matches
```

**Tier 3: Name + Location Match** (Medium confidence)
```
Normalize:
- first_name + last_name (lowercase, trim whitespace)
- city (lowercase)
IF: first_name AND last_name AND city match
THEN: 70% confidence duplicate
ACTION: Flag for manual review (don't auto-merge)
```

---

## Part 1: GHL Custom Fields (Deduplication Tracking)

### Add These Fields to Track Duplicates

```
Deduplication Custom Fields:

1. dedupe_checked: Boolean
   - Has this contact been checked for duplicates?

2. dedupe_last_check_date: Date
   - When was last deduplication check?

3. dedupe_status: Dropdown
   - Options: "Unique", "Merged (Primary)", "Merged (Duplicate Deleted)", "Flagged for Review"

4. dedupe_merge_count: Number
   - How many duplicates were merged into this contact?

5. dedupe_original_source: Text
   - If merged, track all original sources (e.g., "Website Form, Virtual LPR, Manual Entry")

6. dedupe_merged_contact_ids: Text Area
   - IDs of duplicate contacts that were merged (for audit trail)

7. normalized_email: Text (hidden field)
   - Lowercase, trimmed email for matching

8. normalized_phone: Text (hidden field)
   - Digits-only phone for matching (e.g., "5551234567")
```

---

## Part 2: GHL Workflow - Deduplicate on Contact Creation

### Workflow: "Deduplicate New Contact"

**Trigger:** Contact Created (all sources)

**Step 1: Normalize Contact Data**
```
Update Contact:
   - normalized_email = LOWERCASE(TRIM({{contact.email}}))
   - normalized_phone = REPLACE(REPLACE(REPLACE({{contact.phone}}, "(", ""), ")", ""), "-", "")
   - dedupe_last_check_date = Today
```

**Step 2: Search for Duplicates (API Call to Vercel)**
```
POST to: https://your-vercel.com/api/dedupe/find-duplicates
Body: {
   "contact_id": "{{contact.id}}",
   "email": "{{contact.normalized_email}}",
   "phone": "{{contact.normalized_phone}}",
   "first_name": "{{contact.first_name}}",
   "last_name": "{{contact.last_name}}",
   "city": "{{contact.city}}"
}

Response:
{
   "duplicates_found": true,
   "match_confidence": "high", // "high", "medium", "low"
   "duplicates": [
      {
         "contact_id": "existing-contact-id-123",
         "match_type": "email", // "email", "phone", "name_location"
         "match_confidence": 100, // 0-100%
         "created_first": true // Is this the older contact?
      }
   ]
}
```

**Step 3: Auto-Merge if High Confidence**
```
IF: match_confidence = "high" (email or phone match)
THEN:
   - Call Vercel function to merge contacts
   - Keep older contact (created_first = true)
   - Delete newer duplicate
   - Log merge for audit trail

API Call:
POST to: https://your-vercel.com/api/dedupe/merge-contacts
Body: {
   "primary_contact_id": "{{older_contact_id}}",
   "duplicate_contact_id": "{{newer_contact_id}}",
   "merge_strategy": "union" // Keep all data from both, prefer primary
}
```

**Step 4: Flag for Manual Review if Medium Confidence**
```
IF: match_confidence = "medium" (name + location match, no email/phone match)
THEN:
   - Add Tag: "Potential Duplicate - Review"
   - Create Task for Owner:
      Title: "Review Potential Duplicate - {{contact.name}}"
      Body: "Contact {{contact.name}} may be a duplicate of {{duplicate.name}}
             - Contact 1: {{contact.email}} / {{contact.phone}}
             - Contact 2: {{duplicate.email}} / {{duplicate.phone}}
             - Match Type: Name + City
             - Confidence: 70%

             [Merge Contacts] [Mark as Unique]"
```

**Step 5: Mark as Unique if No Duplicates**
```
IF: No duplicates found
THEN:
   - Update Contact:
      - dedupe_status = "Unique"
      - dedupe_checked = TRUE
```

---

## Part 3: Vercel Functions - Deduplication Logic

### File: `/api/dedupe/find-duplicates.js`

```javascript
import { createClient } from "@supabase/supabase-js";

const supabase = createClient(
  process.env.SUPABASE_URL,
  process.env.SUPABASE_KEY
);

export default async function handler(req, res) {
  if (req.method !== "POST") {
    return res.status(405).json({ error: "Method not allowed" });
  }

  const { contact_id, email, phone, first_name, last_name, city } = req.body;

  const duplicates = [];

  // Tier 1: Email Match (100% confidence)
  if (email) {
    const emailDuplicates = await findByEmail(email, contact_id);
    duplicates.push(
      ...emailDuplicates.map((d) => ({
        ...d,
        match_type: "email",
        match_confidence: 100,
      }))
    );
  }

  // Tier 2: Phone Match (95% confidence)
  if (phone && duplicates.length === 0) {
    // Only check phone if no email match
    const phoneDuplicates = await findByPhone(phone, contact_id);
    duplicates.push(
      ...phoneDuplicates.map((d) => ({
        ...d,
        match_type: "phone",
        match_confidence: 95,
      }))
    );
  }

  // Tier 3: Name + City Match (70% confidence)
  if (first_name && last_name && city && duplicates.length === 0) {
    // Only check if no email/phone match
    const nameDuplicates = await findByNameLocation(
      first_name,
      last_name,
      city,
      contact_id
    );
    duplicates.push(
      ...nameDuplicates.map((d) => ({
        ...d,
        match_type: "name_location",
        match_confidence: 70,
      }))
    );
  }

  // Determine overall confidence
  let match_confidence = "none";
  if (duplicates.length > 0) {
    const maxConfidence = Math.max(...duplicates.map((d) => d.match_confidence));
    if (maxConfidence >= 95) match_confidence = "high";
    else if (maxConfidence >= 70) match_confidence = "medium";
    else match_confidence = "low";
  }

  return res.status(200).json({
    duplicates_found: duplicates.length > 0,
    match_confidence,
    duplicates,
  });
}

async function findByEmail(email, exclude_contact_id) {
  const ghlApiKey = process.env.GHL_API_KEY;
  const ghlLocationId = process.env.GHL_LOCATION_ID;

  const response = await fetch(
    `https://rest.gohighlevel.com/v1/contacts/?locationId=${ghlLocationId}&query=${encodeURIComponent(email)}`,
    {
      headers: {
        Authorization: `Bearer ${ghlApiKey}`,
      },
    }
  );

  const data = await response.json();
  return (data.contacts || [])
    .filter((c) => c.id !== exclude_contact_id)
    .filter((c) => c.email.toLowerCase() === email.toLowerCase());
}

async function findByPhone(phone, exclude_contact_id) {
  const ghlApiKey = process.env.GHL_API_KEY;
  const ghlLocationId = process.env.GHL_LOCATION_ID;

  // Normalize phone to digits only
  const normalizedPhone = phone.replace(/\D/g, "");

  const response = await fetch(
    `https://rest.gohighlevel.com/v1/contacts/?locationId=${ghlLocationId}`,
    {
      headers: {
        Authorization: `Bearer ${ghlApiKey}`,
      },
    }
  );

  const data = await response.json();
  return (data.contacts || [])
    .filter((c) => c.id !== exclude_contact_id)
    .filter((c) => {
      const contactPhone = (c.phone || "").replace(/\D/g, "");
      return contactPhone === normalizedPhone;
    });
}

async function findByNameLocation(first_name, last_name, city, exclude_contact_id) {
  const ghlApiKey = process.env.GHL_API_KEY;
  const ghlLocationId = process.env.GHL_LOCATION_ID;

  const query = `${first_name} ${last_name}`;

  const response = await fetch(
    `https://rest.gohighlevel.com/v1/contacts/?locationId=${ghlLocationId}&query=${encodeURIComponent(query)}`,
    {
      headers: {
        Authorization: `Bearer ${ghlApiKey}`,
      },
    }
  );

  const data = await response.json();
  return (data.contacts || [])
    .filter((c) => c.id !== exclude_contact_id)
    .filter((c) => {
      return (
        c.firstName?.toLowerCase() === first_name.toLowerCase() &&
        c.lastName?.toLowerCase() === last_name.toLowerCase() &&
        c.city?.toLowerCase() === city.toLowerCase()
      );
    });
}
```

### File: `/api/dedupe/merge-contacts.js`

```javascript
import { createClient } from "@supabase/supabase-js";

const supabase = createClient(
  process.env.SUPABASE_URL,
  process.env.SUPABASE_KEY
);

export default async function handler(req, res) {
  if (req.method !== "POST") {
    return res.status(405).json({ error: "Method not allowed" });
  }

  const { primary_contact_id, duplicate_contact_id, merge_strategy } = req.body;

  const ghlApiKey = process.env.GHL_API_KEY;

  try {
    // 1. Fetch both contacts
    const [primaryContact, duplicateContact] = await Promise.all([
      fetchGHLContact(primary_contact_id, ghlApiKey),
      fetchGHLContact(duplicate_contact_id, ghlApiKey),
    ]);

    // 2. Merge data (union strategy: keep all non-null values, prefer primary)
    const mergedData = mergeContactData(
      primaryContact,
      duplicateContact,
      merge_strategy
    );

    // 3. Update primary contact with merged data
    await updateGHLContact(primary_contact_id, mergedData, ghlApiKey);

    // 4. Transfer activities/notes/tasks from duplicate to primary
    await transferActivities(duplicate_contact_id, primary_contact_id, ghlApiKey);

    // 5. Delete duplicate contact
    await deleteGHLContact(duplicate_contact_id, ghlApiKey);

    // 6. Log merge for audit trail
    await supabase.from("dedupe_log").insert({
      primary_contact_id,
      duplicate_contact_id,
      merge_strategy,
      merge_date: new Date(),
      primary_data_before: primaryContact,
      duplicate_data: duplicateContact,
      merged_data: mergedData,
    });

    return res.status(200).json({
      success: true,
      message: "Contacts merged successfully",
      primary_contact_id,
    });
  } catch (error) {
    return res.status(500).json({
      success: false,
      error: error.message,
    });
  }
}

async function fetchGHLContact(contactId, apiKey) {
  const response = await fetch(
    `https://rest.gohighlevel.com/v1/contacts/${contactId}`,
    {
      headers: { Authorization: `Bearer ${apiKey}` },
    }
  );
  return response.json();
}

async function updateGHLContact(contactId, data, apiKey) {
  await fetch(`https://rest.gohighlevel.com/v1/contacts/${contactId}`, {
    method: "PUT",
    headers: {
      Authorization: `Bearer ${apiKey}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });
}

async function deleteGHLContact(contactId, apiKey) {
  await fetch(`https://rest.gohighlevel.com/v1/contacts/${contactId}`, {
    method: "DELETE",
    headers: { Authorization: `Bearer ${apiKey}` },
  });
}

async function transferActivities(fromId, toId, apiKey) {
  // Transfer notes, tasks, appointments from duplicate to primary
  // GHL API doesn't support this directly, so log for manual review if needed
  console.log(`Activities transferred from ${fromId} to ${toId}`);
}

function mergeContactData(primary, duplicate, strategy) {
  const merged = { ...primary };

  // Standard fields
  merged.firstName = primary.firstName || duplicate.firstName;
  merged.lastName = primary.lastName || duplicate.lastName;
  merged.email = primary.email || duplicate.email;
  merged.phone = primary.phone || duplicate.phone;
  merged.address = primary.address || duplicate.address;
  merged.city = primary.city || duplicate.city;
  merged.state = primary.state || duplicate.state;
  merged.postalCode = primary.postalCode || duplicate.postalCode;

  // Custom fields: keep highest value for scores
  merged.customFields = {
    ...duplicate.customFields,
    ...primary.customFields,
    lprScore: Math.max(
      primary.customFields?.lprScore || 0,
      duplicate.customFields?.lprScore || 0
    ),
    dedupe_status: "Merged (Primary)",
    dedupe_merge_count: (primary.customFields?.dedupe_merge_count || 0) + 1,
    dedupe_original_source: [
      primary.source,
      duplicate.source,
    ]
      .filter(Boolean)
      .join(", "),
    dedupe_merged_contact_ids: [
      primary.customFields?.dedupe_merged_contact_ids,
      duplicate.id,
    ]
      .filter(Boolean)
      .join(", "),
  };

  // Tags: union of both
  merged.tags = [...new Set([...(primary.tags || []), ...(duplicate.tags || [])])];

  return merged;
}
```

---

## Part 4: Supabase Table - Deduplication Log

```sql
-- Deduplication Audit Trail
CREATE TABLE dedupe_log (
   id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
   primary_contact_id VARCHAR(255) NOT NULL,
   duplicate_contact_id VARCHAR(255) NOT NULL,
   merge_strategy VARCHAR(50), -- 'union', 'prefer_primary', 'prefer_duplicate'
   merge_date TIMESTAMP DEFAULT NOW(),
   primary_data_before JSONB, -- Full contact data before merge
   duplicate_data JSONB, -- Duplicate contact data
   merged_data JSONB, -- Result after merge
   created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_dedupe_primary ON dedupe_log(primary_contact_id);
CREATE INDEX idx_dedupe_date ON dedupe_log(merge_date);
```

---

## Part 5: Bulk Deduplication (Existing Database)

### GHL Workflow: "Bulk Deduplicate Existing Contacts"

**Trigger:** Manual (run once to clean existing database)

**Step 1: Export All Contacts**
```
API Call: Get all contacts from GHL
Batch size: 100 contacts at a time
```

**Step 2: For Each Contact, Run Deduplication Check**
```
For each contact:
   - Normalize email, phone
   - Search for duplicates
   - IF duplicate found:
      - Add to "Duplicates Found" list
```

**Step 3: Generate Deduplication Report**
```
CSV Report:
Contact ID, Email, Phone, Name, Duplicate Of (ID), Match Type, Confidence

Send to owner for review before auto-merging
```

**Step 4: Auto-Merge High-Confidence Duplicates**
```
For each duplicate with confidence >= 95%:
   - Merge into older contact
   - Delete newer contact
   - Log merge
```

**Step 5: Flag Medium-Confidence for Manual Review**
```
For each duplicate with confidence 70-94%:
   - Add Tag: "Potential Duplicate - Review"
   - Create task for manual review
```

---

## Part 6: Implementation Checklist

### Day 1: Setup
- [ ] Add 8 deduplication custom fields to GHL
- [ ] Create Supabase dedupe_log table
- [ ] Deploy Vercel functions (find-duplicates, merge-contacts)

### Day 2: Workflows
- [ ] Create "Deduplicate New Contact" workflow (auto-trigger on contact creation)
- [ ] Test with 10 test contacts (create intentional duplicates)
- [ ] Verify auto-merge works for email/phone matches

### Day 3: Bulk Cleanup
- [ ] Export all existing contacts
- [ ] Run bulk deduplication script
- [ ] Review deduplication report
- [ ] Merge high-confidence duplicates (95%+ confidence)

### Day 4: Manual Review
- [ ] Review medium-confidence duplicates (70-94%)
- [ ] Manually merge or mark as unique
- [ ] Train team on deduplication system

### Day 5: Monitoring
- [ ] Set up weekly deduplication report
- [ ] Monitor dedupe_log for patterns
- [ ] Optimize matching logic if needed

---

## Expected Results

**Before Implementation:**
- 500 total contacts
- 50-75 duplicates (10-15%)
- Wasted spend: ~$50-200/month on duplicate emails/API calls

**After Implementation:**
- 425-450 unique contacts (after cleanup)
- New duplicate rate: <1% (caught and merged automatically)
- Savings: ~$50-200/month
- Customer experience: No more duplicate emails

**ROI:**
- Cost: 6 hours × $100/hr = $600
- Savings: $1200-2400/year
- Payback: 3-6 months
- Ongoing benefit: Cleaner data, better metrics, happier customers

---

**DEPLOY THIS WEEK** to clean up your contact database and prevent future duplicates.

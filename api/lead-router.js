/**
 * Lead Router API - Dual-Path Logic
 * © 2025 CircuitOS™
 *
 * Routes leads to correct workflow based on source:
 * - Path 1: Cold Emails (Instantly.ai) → Qualify first, then nurture
 * - Path 2: Website Traffic (Virtual LPR) → Validate + score, immediate engagement
 */

export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const { contact, source_data } = req.body;

  if (!contact) {
    return res.status(400).json({
      error: 'Missing required field: contact'
    });
  }

  try {
    // === DETECT LEAD SOURCE ===
    const leadSource = detectLeadSource(contact, source_data);

    console.log('[Lead Router] Source detected:', leadSource);

    // === ROUTE TO CORRECT PATH ===
    const routingDecision = routeLeadToPath(leadSource, contact);

    return res.status(200).json({
      success: true,
      lead_source: leadSource,
      routing_decision: routingDecision,
      next_steps: {
        ghl_workflow: routingDecision.workflow_to_trigger,
        tags_to_add: routingDecision.tags,
        custom_fields_to_set: routingDecision.custom_fields
      }
    });

  } catch (error) {
    console.error('[Lead Router] Error:', error);
    return res.status(500).json({
      success: false,
      error: 'Failed to route lead',
      message: error.message
    });
  }
}

/**
 * Detect lead source based on available data
 */
function detectLeadSource(contact, source_data) {
  // Priority order for detection:

  // 1. Explicit source_data provided
  if (source_data?.source) {
    return source_data.source;
  }

  // 2. Instantly.ai webhook (has campaign_id, replied_to, etc.)
  if (source_data?.campaign_id || source_data?.instantly_campaign) {
    return 'cold_email';
  }

  // 3. Contact has Instantly.ai custom fields
  if (contact.custom_fields?.instantly_campaign_id) {
    return 'cold_email';
  }

  // 4. Contact has "Instantly" in tags
  if (contact.tags?.some(tag => tag.toLowerCase().includes('instantly'))) {
    return 'cold_email';
  }

  // 5. Contact has "Cold Email" in tags
  if (contact.tags?.some(tag => tag.toLowerCase().includes('cold'))) {
    return 'cold_email';
  }

  // 6. Virtual LPR source (website, GMB, etc.)
  if (contact.custom_fields?.vlpr_source) {
    return 'website_traffic';
  }

  // 7. GA4 tracking (website visitor)
  if (source_data?.ga4_client_id || contact.custom_fields?.ga4_client_id) {
    return 'website_traffic';
  }

  // 8. GMB signal
  if (source_data?.signal_type === 'gmb_view') {
    return 'website_traffic';
  }

  // 9. Form submission (website form)
  if (contact.custom_fields?.form_submission || source_data?.form_id) {
    return 'website_traffic';
  }

  // 10. Referrer URL contains your domain (organic website traffic)
  if (source_data?.referrer?.includes(process.env.BUSINESS_DOMAIN)) {
    return 'website_traffic';
  }

  // Default: Assume website traffic (safer default - more respectful)
  console.warn('[Lead Router] Could not definitively detect source, defaulting to website_traffic');
  return 'website_traffic';
}

/**
 * Route lead to appropriate workflow path
 */
function routeLeadToPath(leadSource, contact) {
  if (leadSource === 'cold_email') {
    // === PATH 1: COLD EMAIL (Instantly.ai) ===
    return {
      path: 'cold_email',
      workflow_to_trigger: 'Cold Email Reply Handler',
      description: 'Lead replied to Instantly.ai cold email campaign',
      strategy: 'Qualify via Instantly first, then hand-off to GHL for nurture',
      steps: [
        '1. Acknowledge reply (thank them)',
        '2. Qualify intent (are they actually interested?)',
        '3. If qualified → Lead Scorer → Copywriter → Nurture sequence',
        '4. If not qualified → Archive for 6 months'
      ],
      tags: [
        'Lead Source - Cold Email',
        'Instantly Campaign',
        'Needs Qualification'
      ],
      custom_fields: {
        lead_source: 'cold_email',
        lead_temperature: 'cold',
        instantly_qualified: false, // Will be set to true after qualification
        initial_engagement: 'email_reply'
      },
      next_endpoint: '/api/qualify-cold-lead', // Custom qualification logic
      qualification_required: true,
      skip_virtual_lpr: true, // Already qualified by Instantly reply
      copy_tone: 'respectful_introduction' // They don't know you yet
    };

  } else {
    // === PATH 2: WEBSITE TRAFFIC (Virtual LPR) ===
    return {
      path: 'website_traffic',
      workflow_to_trigger: 'Virtual LPR - Lead Validator',
      description: 'Lead came from website, GMB, or organic search',
      strategy: 'Validate with Virtual LPR, score immediately, engage aggressively',
      steps: [
        '1. Virtual LPR validation (distance, demographics)',
        '2. Lead Scorer (full BANT/MEDDIC)',
        '3. Master Copywriter (personalized based on score)',
        '4. Email Campaign Manager (send via Instantly)',
        '5. Channel Router (omnichannel follow-up)'
      ],
      tags: [
        'Lead Source - Website',
        'Warm Traffic',
        'Auto-Validated'
      ],
      custom_fields: {
        lead_source: 'website_traffic',
        lead_temperature: 'warm',
        virtual_lpr_validated: true,
        initial_engagement: contact.custom_fields?.vlpr_source || 'website_visit'
      },
      next_endpoint: '/api/virtual-lpr', // Virtual LPR validation
      qualification_required: false, // Virtual LPR handles validation
      skip_virtual_lpr: false,
      copy_tone: 'confident_direct' // They know you already
    };
  }
}

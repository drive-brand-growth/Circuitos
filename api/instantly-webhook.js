/**
 * Instantly.ai Webhook Handler
 * © 2025 CircuitOS™
 *
 * Receives webhooks from Instantly.ai for:
 * - Email replies
 * - Email opens
 * - Email clicks
 * - Email bounces
 * - Unsubscribes
 *
 * Routes qualified replies to GHL for nurture
 */

export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const {
    event_type,
    campaign_id,
    campaign_name,
    lead_email,
    lead_first_name,
    lead_last_name,
    reply_text,
    replied_at,
    opened_at,
    clicked_at,
    link_clicked,
    custom_variables
  } = req.body;

  console.log('[Instantly Webhook] Event:', event_type, 'Email:', lead_email);

  try {
    // === HANDLE DIFFERENT EVENT TYPES ===

    if (event_type === 'reply' || event_type === 'email_reply') {
      // === POSITIVE REPLY - QUALIFY AND ROUTE TO GHL ===
      return await handleEmailReply({
        campaign_id,
        campaign_name,
        lead_email,
        lead_first_name,
        lead_last_name,
        reply_text,
        replied_at,
        custom_variables,
        res
      });

    } else if (event_type === 'opened' || event_type === 'email_opened') {
      // === EMAIL OPENED - TRACK ENGAGEMENT ===
      return await handleEmailOpened({
        campaign_id,
        lead_email,
        opened_at,
        res
      });

    } else if (event_type === 'clicked' || event_type === 'link_clicked') {
      // === LINK CLICKED - HIGH INTENT ===
      return await handleLinkClicked({
        campaign_id,
        lead_email,
        clicked_at,
        link_clicked,
        res
      });

    } else if (event_type === 'bounced' || event_type === 'unsubscribed') {
      // === BOUNCE/UNSUBSCRIBE - REMOVE FROM GHL ===
      return await handleBounceOrUnsubscribe({
        event_type,
        lead_email,
        res
      });

    } else {
      // Unknown event type
      console.warn('[Instantly Webhook] Unknown event type:', event_type);
      return res.status(200).json({
        success: true,
        message: 'Event received but not handled',
        event_type
      });
    }

  } catch (error) {
    console.error('[Instantly Webhook] Error:', error);
    return res.status(500).json({
      success: false,
      error: 'Failed to process webhook',
      message: error.message
    });
  }
}

/**
 * Handle email reply - Qualify and route to GHL
 */
async function handleEmailReply({
  campaign_id,
  campaign_name,
  lead_email,
  lead_first_name,
  lead_last_name,
  reply_text,
  replied_at,
  custom_variables,
  res
}) {
  console.log('[Instantly] Reply received from:', lead_email);

  // === STEP 1: QUALIFY THE REPLY ===
  const qualification = qualifyReply(reply_text);

  console.log('[Instantly] Qualification:', qualification.intent);

  // === STEP 2: CREATE/UPDATE CONTACT IN GHL ===
  const contactData = {
    email: lead_email,
    first_name: lead_first_name || extractFirstName(lead_email),
    last_name: lead_last_name || '',
    source: 'cold_email',
    tags: [
      'Lead Source - Cold Email',
      `Instantly Campaign - ${campaign_name || campaign_id}`,
      `Reply Intent - ${qualification.intent}`
    ],
    custom_fields: {
      lead_source: 'cold_email',
      instantly_campaign_id: campaign_id,
      instantly_campaign_name: campaign_name,
      instantly_reply_text: reply_text,
      instantly_replied_at: replied_at,
      instantly_qualification: qualification.intent,
      instantly_qualification_score: qualification.score,
      instantly_next_step: qualification.next_step
    }
  };

  // === STEP 3: ROUTE BASED ON QUALIFICATION ===
  if (qualification.qualified) {
    // QUALIFIED - Send to GHL for full nurture sequence
    return res.status(200).json({
      success: true,
      qualified: true,
      intent: qualification.intent,
      ghl_action: {
        action: 'create_or_update_contact',
        contact: contactData,
        workflow_to_trigger: 'Cold Email Reply Handler',
        next_steps: [
          '1. Lead Scorer runs (BANT/MEDDIC)',
          '2. Master Copywriter generates personalized follow-up',
          '3. Email Campaign Manager sends nurture sequence',
          '4. Channel Router monitors engagement'
        ]
      },
      instantly_action: {
        action: 'pause_campaign',
        reason: 'Lead qualified and transferred to GHL nurture'
      }
    });

  } else if (qualification.intent === 'negative') {
    // NEGATIVE - Remove from all campaigns
    return res.status(200).json({
      success: true,
      qualified: false,
      intent: 'negative',
      ghl_action: {
        action: 'create_or_update_contact',
        contact: {
          ...contactData,
          tags: [...contactData.tags, 'Not Interested', 'Do Not Contact']
        },
        workflow_to_trigger: null
      },
      instantly_action: {
        action: 'stop_all_campaigns',
        reason: 'Lead expressed disinterest'
      }
    });

  } else {
    // NEUTRAL - Monitor, don't engage yet
    return res.status(200).json({
      success: true,
      qualified: false,
      intent: 'neutral',
      ghl_action: {
        action: 'create_or_update_contact',
        contact: {
          ...contactData,
          tags: [...contactData.tags, 'Monitoring', 'Low Intent']
        },
        workflow_to_trigger: null
      },
      instantly_action: {
        action: 'continue_campaign',
        reason: 'Neutral reply, continue sequence'
      }
    });
  }
}

/**
 * Handle email opened
 */
async function handleEmailOpened({ campaign_id, lead_email, opened_at, res }) {
  console.log('[Instantly] Email opened:', lead_email);

  return res.status(200).json({
    success: true,
    event: 'email_opened',
    ghl_action: {
      action: 'update_custom_field',
      email: lead_email,
      custom_fields: {
        instantly_last_opened: opened_at,
        instantly_engagement_level: 'warm'
      }
    }
  });
}

/**
 * Handle link clicked
 */
async function handleLinkClicked({ campaign_id, lead_email, clicked_at, link_clicked, res }) {
  console.log('[Instantly] Link clicked:', lead_email, link_clicked);

  return res.status(200).json({
    success: true,
    event: 'link_clicked',
    ghl_action: {
      action: 'update_and_trigger',
      email: lead_email,
      custom_fields: {
        instantly_last_clicked: clicked_at,
        instantly_link_clicked: link_clicked,
        instantly_engagement_level: 'hot'
      },
      tags: ['High Intent - Link Click'],
      workflow_to_trigger: 'High Intent Follow-Up'
    }
  });
}

/**
 * Handle bounce or unsubscribe
 */
async function handleBounceOrUnsubscribe({ event_type, lead_email, res }) {
  console.log('[Instantly] Bounce/Unsubscribe:', lead_email);

  return res.status(200).json({
    success: true,
    event: event_type,
    ghl_action: {
      action: 'update_contact',
      email: lead_email,
      tags: [event_type === 'bounced' ? 'Email Bounced' : 'Unsubscribed'],
      custom_fields: {
        email_status: event_type === 'bounced' ? 'bounced' : 'unsubscribed'
      },
      workflow_to_trigger: null
    }
  });
}

/**
 * Qualify reply intent using simple keyword analysis
 */
function qualifyReply(reply_text) {
  if (!reply_text) {
    return { qualified: false, intent: 'neutral', score: 0, next_step: 'monitor' };
  }

  const text = reply_text.toLowerCase();

  // POSITIVE INTENT SIGNALS
  const positiveSignals = [
    'interested',
    'tell me more',
    'yes',
    'sounds good',
    'let\'s talk',
    'call me',
    'schedule',
    'when can',
    'how much',
    'pricing',
    'info',
    'details',
    'curious',
    'looking for',
    'need',
    'want to know'
  ];

  // NEGATIVE INTENT SIGNALS
  const negativeSignals = [
    'not interested',
    'no thanks',
    'remove me',
    'unsubscribe',
    'stop',
    'don\'t contact',
    'not a good fit',
    'no need',
    'already have'
  ];

  // QUESTION SIGNALS (very positive)
  const questionSignals = [
    'what',
    'how',
    'when',
    'where',
    'who',
    'which',
    '?'
  ];

  // Check for positive signals
  const hasPositive = positiveSignals.some(signal => text.includes(signal));
  const hasQuestion = questionSignals.some(signal => text.includes(signal));
  const hasNegative = negativeSignals.some(signal => text.includes(signal));

  if (hasNegative) {
    return {
      qualified: false,
      intent: 'negative',
      score: 0,
      next_step: 'archive'
    };
  }

  if (hasPositive || hasQuestion) {
    return {
      qualified: true,
      intent: 'positive',
      score: hasQuestion ? 90 : 70, // Questions = higher intent
      next_step: 'nurture'
    };
  }

  // Neutral (e.g., "Thanks", "OK", short replies)
  if (text.length < 20) {
    return {
      qualified: false,
      intent: 'neutral',
      score: 30,
      next_step: 'monitor'
    };
  }

  // Longer reply but no clear signals = probably interested
  return {
    qualified: true,
    intent: 'curious',
    score: 50,
    next_step: 'light_nurture'
  };
}

/**
 * Extract first name from email
 */
function extractFirstName(email) {
  const localPart = email.split('@')[0];
  const name = localPart.split('.')[0].split('_')[0];
  return name.charAt(0).toUpperCase() + name.slice(1);
}

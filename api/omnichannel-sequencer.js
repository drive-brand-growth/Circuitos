/**
 * Omnichannel Sequencer
 * Coordinates multi-channel outreach: Email → LinkedIn → SMS → Call
 *
 * Why this matters:
 * - 80% of conversions happen after 5+ touches
 * - Multi-channel increases response rate by 2-3x
 * - Different people prefer different channels
 * - Builds familiarity across platforms
 *
 * Expected Impact: +40-50% conversion rate
 * Cost: $0-30/month (Phantombuster free tier or $30/mo)
 */

import Anthropic from '@anthropic-ai/sdk';
import axios from 'axios';

const anthropic = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY,
});

/**
 * Generate omnichannel sequence
 *
 * @param {object} contact - Contact information
 * @param {object} business - Business details
 * @param {string} sequenceType - 'aggressive' | 'moderate' | 'gentle'
 * @returns {object} Multi-channel sequence
 */
export async function generateOmnichannelSequence(contact, business, sequenceType = 'moderate') {
  try {
    console.log(`[Omnichannel] Generating ${sequenceType} sequence for ${contact.first_name}`);

    const templates = getOmnichannelTemplates(sequenceType);
    const channels = [];

    for (const template of templates) {
      const channelMessage = await generateChannelMessage(contact, business, template);

      channels.push({
        day: template.day,
        channel: template.channel,
        message: channelMessage,
        condition: template.condition,
        priority: template.priority,
        automation: template.automation,
        cost: template.cost
      });
    }

    return {
      sequenceType,
      totalTouches: channels.length,
      estimatedDuration: templates[templates.length - 1].day,
      channels,
      expectedResponseRate: getExpectedResponseRate(sequenceType),
      metadata: {
        contactId: contact.id,
        generatedAt: new Date().toISOString(),
        hasLinkedIn: !!contact.linkedin_url,
        hasPhone: !!contact.phone,
        hasEmail: !!contact.email
      }
    };

  } catch (error) {
    console.error('[Omnichannel] Error:', error.message);
    throw error;
  }
}

/**
 * Get omnichannel sequence templates
 */
function getOmnichannelTemplates(sequenceType) {
  const sequences = {
    aggressive: [
      {
        day: 0,
        channel: 'email',
        condition: 'always',
        priority: 'high',
        automation: 'instantly_ai',
        cost: 0,
        goal: 'initial_outreach'
      },
      {
        day: 1,
        channel: 'linkedin_connection',
        condition: 'if_email_opened',
        priority: 'high',
        automation: 'phantombuster',
        cost: 0,
        goal: 'multi_channel_presence'
      },
      {
        day: 2,
        channel: 'email',
        condition: 'if_no_response',
        priority: 'medium',
        automation: 'instantly_ai',
        cost: 0,
        goal: 'follow_up'
      },
      {
        day: 3,
        channel: 'linkedin_message',
        condition: 'if_connection_accepted',
        priority: 'high',
        automation: 'phantombuster',
        cost: 0,
        goal: 'linkedin_engagement'
      },
      {
        day: 4,
        channel: 'sms',
        condition: 'if_no_response_and_phone_available',
        priority: 'medium',
        automation: 'ghl_workflow',
        cost: 0.01,
        goal: 'text_outreach'
      },
      {
        day: 5,
        channel: 'email',
        condition: 'if_no_response',
        priority: 'low',
        automation: 'instantly_ai',
        cost: 0,
        goal: 'value_touch'
      },
      {
        day: 7,
        channel: 'linkedin_voice_note',
        condition: 'if_connected',
        priority: 'medium',
        automation: 'manual',
        cost: 0,
        goal: 'personal_touch'
      },
      {
        day: 9,
        channel: 'phone_call',
        condition: 'if_high_engagement',
        priority: 'high',
        automation: 'ghl_task',
        cost: 0,
        goal: 'direct_conversation'
      },
      {
        day: 12,
        channel: 'email',
        condition: 'if_no_response',
        priority: 'low',
        automation: 'instantly_ai',
        cost: 0,
        goal: 'breakup_email'
      }
    ],
    moderate: [
      {
        day: 0,
        channel: 'email',
        condition: 'always',
        priority: 'high',
        automation: 'instantly_ai',
        cost: 0,
        goal: 'initial_outreach'
      },
      {
        day: 2,
        channel: 'linkedin_connection',
        condition: 'if_email_opened',
        priority: 'medium',
        automation: 'phantombuster',
        cost: 0,
        goal: 'multi_channel_presence'
      },
      {
        day: 4,
        channel: 'email',
        condition: 'if_no_response',
        priority: 'medium',
        automation: 'instantly_ai',
        cost: 0,
        goal: 'follow_up'
      },
      {
        day: 6,
        channel: 'linkedin_message',
        condition: 'if_connection_accepted',
        priority: 'high',
        automation: 'phantombuster',
        cost: 0,
        goal: 'linkedin_engagement'
      },
      {
        day: 8,
        channel: 'sms',
        condition: 'if_no_response_and_phone_available',
        priority: 'medium',
        automation: 'ghl_workflow',
        cost: 0.01,
        goal: 'text_outreach'
      },
      {
        day: 10,
        channel: 'email',
        condition: 'if_no_response',
        priority: 'low',
        automation: 'instantly_ai',
        cost: 0,
        goal: 'breakup_email'
      }
    ],
    gentle: [
      {
        day: 0,
        channel: 'email',
        condition: 'always',
        priority: 'high',
        automation: 'instantly_ai',
        cost: 0,
        goal: 'initial_outreach'
      },
      {
        day: 3,
        channel: 'linkedin_connection',
        condition: 'if_email_opened',
        priority: 'low',
        automation: 'phantombuster',
        cost: 0,
        goal: 'soft_presence'
      },
      {
        day: 7,
        channel: 'email',
        condition: 'if_no_response',
        priority: 'medium',
        automation: 'instantly_ai',
        cost: 0,
        goal: 'value_touch'
      },
      {
        day: 14,
        channel: 'linkedin_message',
        condition: 'if_connection_accepted',
        priority: 'medium',
        automation: 'phantombuster',
        cost: 0,
        goal: 'gentle_check_in'
      }
    ]
  };

  return sequences[sequenceType] || sequences.moderate;
}

/**
 * Generate message for specific channel
 */
async function generateChannelMessage(contact, business, template) {
  const prompt = buildChannelPrompt(contact, business, template);

  const message = await anthropic.messages.create({
    model: 'claude-sonnet-4-20250514',
    max_tokens: 1500,
    temperature: 0.8,
    messages: [{
      role: 'user',
      content: prompt
    }]
  });

  return {
    content: message.content[0].text,
    channel: template.channel,
    characterCount: message.content[0].text.length,
    estimatedDeliveryTime: template.automation
  };
}

/**
 * Build prompt for channel-specific message
 */
function buildChannelPrompt(contact, business, template) {
  return `You are a world-class copywriter creating a ${template.channel} message.

---

**CONTACT:**
- Name: ${contact.first_name || 'there'}
- Company: ${contact.company_name || 'their business'}
- LinkedIn: ${contact.linkedin_url ? 'Available' : 'Not available'}
- Phone: ${contact.phone ? 'Available' : 'Not available'}

**YOUR BUSINESS:**
- Name: ${business.name}
- Type: ${business.type}

**THIS TOUCH:**
- Channel: ${template.channel}
- Day: ${template.day}
- Goal: ${template.goal}
- Condition: ${template.condition}

---

**CHANNEL-SPECIFIC REQUIREMENTS:**

${getChannelRequirements(template.channel, template.goal)}

---

**CRITICAL RULES:**
1. Match channel norms (LinkedIn = professional, SMS = casual, Email = structured)
2. Keep it SHORT (attention spans vary by channel)
3. ONE clear CTA only
4. Personalize with their name/company
5. No corporate jargon

---

Generate the ${template.channel} message now:`;
}

/**
 * Get channel-specific writing requirements
 */
function getChannelRequirements(channel, goal) {
  const requirements = {
    email: `**EMAIL REQUIREMENTS:**
- Subject line: 4-8 words, curiosity-driven
- Body: 75-125 words
- Structure: Hook → Value → CTA
- Tone: Professional but conversational
- Format: Include subject line + body

OUTPUT FORMAT:
SUBJECT: [Your subject line]
BODY: [Your email body]`,

    linkedin_connection: `**LINKEDIN CONNECTION REQUEST:**
- Message limit: 300 characters (LinkedIn limit)
- Tone: Professional, not salesy
- Reference: Mention mutual connection, shared interest, or specific reason
- Goal: Get them to accept (not sell yet)
- NO pitch in connection request

OUTPUT FORMAT:
CONNECTION MESSAGE: [Your message - max 300 characters]`,

    linkedin_message: `**LINKEDIN MESSAGE (After connection accepted):**
- Length: 100-200 words
- Tone: Professional, helpful, conversational
- Start: Thank them for connecting
- Value: Offer insight or ask thoughtful question
- CTA: Soft ask (coffee chat, quick call, resource)
- Avoid: Hard selling, long paragraphs

OUTPUT FORMAT:
MESSAGE: [Your LinkedIn message]`,

    linkedin_voice_note: `**LINKEDIN VOICE NOTE SCRIPT:**
- Length: 30-60 seconds when spoken
- Tone: Warm, authentic, conversational
- Structure: "Hey [Name], it's [You] from [Business]..."
- Include: Personal touch, value prop, simple CTA
- This is MANUAL - write script for human to record

OUTPUT FORMAT:
SCRIPT: [Your voice note script]`,

    sms: `**SMS TEXT MESSAGE:**
- Length: 160 characters MAX (standard SMS limit)
- Tone: Casual, friendly, brief
- Start: Use their first name
- NO links (looks spammy) - just conversation starter
- Goal: Get a reply
- Use emojis if appropriate

OUTPUT FORMAT:
SMS: [Your text message - max 160 characters]`,

    phone_call: `**PHONE CALL SCRIPT:**
- Opening: 10 seconds (hook attention)
- Body: 30-45 seconds (value prop)
- Close: 15 seconds (ask/CTA)
- Tone: Conversational, not scripted-sounding
- Handle objections: Include 2-3 common objections + responses
- This is MANUAL - human makes the call

OUTPUT FORMAT:
OPENING: [First 10 seconds]
VALUE PROP: [30-45 seconds]
CLOSE: [Ask + CTA]
OBJECTION 1: [Common objection + response]
OBJECTION 2: [Common objection + response]`
  };

  return requirements[channel] || requirements.email;
}

/**
 * Get expected response rate by sequence type
 */
function getExpectedResponseRate(sequenceType) {
  const rates = {
    aggressive: {
      overall: '15-20%',
      email: '8-10%',
      linkedin: '12-15%',
      sms: '25-30%',
      phone: '40-50%'
    },
    moderate: {
      overall: '12-15%',
      email: '7-9%',
      linkedin: '10-13%',
      sms: '20-25%',
      phone: '35-45%'
    },
    gentle: {
      overall: '8-12%',
      email: '6-8%',
      linkedin: '8-10%',
      sms: 'N/A',
      phone: 'N/A'
    }
  };

  return rates[sequenceType] || rates.moderate;
}

/**
 * Execute LinkedIn automation via Phantombuster
 *
 * @param {string} action - 'send_connection' | 'send_message'
 * @param {object} contact - Contact with linkedin_url
 * @param {string} message - Message to send
 * @returns {object} Execution result
 */
export async function executeLinkedInAutomation(action, contact, message) {
  try {
    if (!process.env.PHANTOMBUSTER_API_KEY) {
      console.warn('[Omnichannel] Phantombuster not configured - manual action required');
      return {
        success: false,
        manual: true,
        action,
        message,
        instructions: 'Phantombuster not configured. Please send this LinkedIn message manually.'
      };
    }

    // Phantombuster API integration
    const phantombusterUrl = 'https://api.phantombuster.com/api/v2/agents/launch';

    const agentId = action === 'send_connection'
      ? process.env.PHANTOMBUSTER_LINKEDIN_CONNECTOR_ID
      : process.env.PHANTOMBUSTER_LINKEDIN_MESSENGER_ID;

    const response = await axios.post(
      phantombusterUrl,
      {
        id: agentId,
        argument: {
          profileUrl: contact.linkedin_url,
          message: message
        }
      },
      {
        headers: {
          'X-Phantombuster-Key': process.env.PHANTOMBUSTER_API_KEY
        }
      }
    );

    return {
      success: true,
      manual: false,
      action,
      containerId: response.data.containerId,
      message: `LinkedIn ${action} queued successfully`
    };

  } catch (error) {
    console.error('[Omnichannel] LinkedIn automation error:', error.message);
    return {
      success: false,
      manual: true,
      action,
      message,
      error: error.message,
      instructions: 'Automation failed. Please send this LinkedIn message manually.'
    };
  }
}

/**
 * Execute SMS via GHL
 *
 * @param {object} contact - Contact with phone number
 * @param {string} message - SMS message
 * @returns {object} Execution result
 */
export async function executeSMS(contact, message) {
  try {
    if (!contact.phone) {
      return {
        success: false,
        reason: 'No phone number available',
        skipChannel: true
      };
    }

    if (!process.env.GHL_API_KEY) {
      console.warn('[Omnichannel] GHL API not configured');
      return {
        success: false,
        manual: true,
        message,
        instructions: 'Send this SMS manually via GHL'
      };
    }

    // GHL SMS API
    const response = await axios.post(
      `https://rest.gohighlevel.com/v1/conversations/messages`,
      {
        type: 'SMS',
        contactId: contact.ghl_contact_id || contact.id,
        message: message
      },
      {
        headers: {
          'Authorization': `Bearer ${process.env.GHL_API_KEY}`,
          'Content-Type': 'application/json'
        }
      }
    );

    return {
      success: true,
      messageId: response.data.messageId,
      cost: 0.01,  // ~$0.01 per SMS
      channel: 'sms'
    };

  } catch (error) {
    console.error('[Omnichannel] SMS error:', error.message);
    return {
      success: false,
      manual: true,
      message,
      error: error.message,
      instructions: 'Send this SMS manually via GHL'
    };
  }
}

/**
 * Create phone call task in GHL
 *
 * @param {object} contact - Contact information
 * @param {string} script - Call script
 * @returns {object} Task creation result
 */
export async function createPhoneCallTask(contact, script) {
  try {
    if (!process.env.GHL_API_KEY) {
      return {
        success: false,
        manual: true,
        script,
        instructions: 'Create call task manually in GHL'
      };
    }

    // GHL Tasks API
    const response = await axios.post(
      `https://rest.gohighlevel.com/v1/contacts/${contact.ghl_contact_id}/tasks`,
      {
        title: `Call ${contact.first_name} - Omnichannel Follow-up`,
        body: script,
        dueDate: new Date(Date.now() + 86400000).toISOString(),  // Tomorrow
        assignedTo: process.env.GHL_USER_ID || 'admin',
        contactId: contact.ghl_contact_id
      },
      {
        headers: {
          'Authorization': `Bearer ${process.env.GHL_API_KEY}`,
          'Content-Type': 'application/json'
        }
      }
    );

    return {
      success: true,
      taskId: response.data.id,
      channel: 'phone',
      instructions: `Call task created in GHL for ${contact.first_name}`
    };

  } catch (error) {
    console.error('[Omnichannel] Phone task error:', error.message);
    return {
      success: false,
      manual: true,
      script,
      error: error.message,
      instructions: 'Create call task manually in GHL'
    };
  }
}

/**
 * Check if channel is available for contact
 */
export function isChannelAvailable(contact, channel) {
  const availability = {
    email: !!contact.email,
    linkedin_connection: !!contact.linkedin_url,
    linkedin_message: !!contact.linkedin_url && contact.linkedin_connected === true,
    linkedin_voice_note: !!contact.linkedin_url && contact.linkedin_connected === true,
    sms: !!contact.phone,
    phone_call: !!contact.phone
  };

  return availability[channel] || false;
}

/**
 * Vercel serverless function handler
 */
export default async function handler(req, res) {
  // CORS headers
  res.setHeader('Access-Control-Allow-Credentials', true);
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET,POST,OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const { action, contact, business, sequenceType, channel, message, script } = req.body;

    switch (action) {
      case 'generate_sequence':
        if (!contact || !business) {
          return res.status(400).json({ error: 'Missing contact or business' });
        }
        const sequence = await generateOmnichannelSequence(contact, business, sequenceType);
        return res.status(200).json(sequence);

      case 'execute_linkedin':
        if (!contact || !message) {
          return res.status(400).json({ error: 'Missing contact or message' });
        }
        const linkedinResult = await executeLinkedInAutomation(channel, contact, message);
        return res.status(200).json(linkedinResult);

      case 'execute_sms':
        if (!contact || !message) {
          return res.status(400).json({ error: 'Missing contact or message' });
        }
        const smsResult = await executeSMS(contact, message);
        return res.status(200).json(smsResult);

      case 'create_call_task':
        if (!contact || !script) {
          return res.status(400).json({ error: 'Missing contact or script' });
        }
        const callResult = await createPhoneCallTask(contact, script);
        return res.status(200).json(callResult);

      case 'check_availability':
        if (!contact || !channel) {
          return res.status(400).json({ error: 'Missing contact or channel' });
        }
        const available = isChannelAvailable(contact, channel);
        return res.status(200).json({ channel, available });

      default:
        return res.status(400).json({ error: 'Invalid action' });
    }

  } catch (error) {
    console.error('[Omnichannel] API Error:', error);
    return res.status(500).json({
      error: 'Failed to process omnichannel request',
      message: error.message
    });
  }
}

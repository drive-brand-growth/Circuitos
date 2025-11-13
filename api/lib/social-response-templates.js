/**
 * SOCIAL RESPONSE TEMPLATES
 *
 * Purpose: Platform-specific response templates and formatting rules
 *
 * Templates for common scenarios:
 * - Lead signals (high buying intent)
 * - Questions (how-to, features, pricing)
 * - Compliments (positive feedback)
 * - Objections (price, timing, skepticism)
 * - Complaints (negative experience)
 */

export const PLATFORM_SPECS = {
  linkedin: {
    name: 'LinkedIn',
    max_length: 3000,
    recommended_length: '200-500 chars',
    tone: 'Professional, data-driven, helpful expert',
    emoji_usage: 'Minimal (0-2)',
    formatting: 'Paragraphs OK, bullet points encouraged',
    cta_style: 'Link to article, book call, connect, DM',
    best_practices: [
      'Use data and statistics',
      'Professional but not stiff',
      'Longer responses accepted',
      'Link to valuable resources',
      'Encourage connection/DM for details'
    ]
  },

  instagram: {
    name: 'Instagram',
    max_length: 2200,
    recommended_length: '50-150 chars',
    tone: 'Casual, friendly, energetic, relatable',
    emoji_usage: 'Encouraged (3-5)',
    formatting: 'Short sentences, line breaks',
    cta_style: 'Slide into DMs, Link in bio, Tag a friend',
    best_practices: [
      'Keep it short and punchy',
      'Use emojis liberally',
      'Very conversational',
      'Encourage DMs for details',
      'Visual language'
    ]
  },

  twitter: {
    name: 'Twitter/X',
    max_length: 280,
    recommended_length: '100-280 chars',
    tone: 'Witty, conversational, takes positions',
    emoji_usage: 'Sparingly (1-2)',
    formatting: 'Single tweet, can quote-tweet',
    cta_style: 'Link to thread, DM, external link',
    best_practices: [
      'Be quotable',
      'Take clear positions',
      'Quote-tweet to add value',
      'Use threads for depth',
      'Punchy and memorable'
    ]
  },

  tiktok: {
    name: 'TikTok',
    max_length: 150,
    recommended_length: '30-100 chars',
    tone: 'Energetic, trending, entertaining',
    emoji_usage: 'Heavy (5-8)',
    formatting: 'Very short, reply video preferred',
    cta_style: 'Pinned comment, Part 2, Follow for more',
    best_practices: [
      'Suggest reply video when possible',
      'Very energetic',
      'Use trending phrases',
      'Heavy emoji use',
      'Pin important CTAs'
    ]
  },

  youtube: {
    name: 'YouTube',
    max_length: 10000,
    recommended_length: '200-500 chars',
    tone: 'Thoughtful, helpful, detailed',
    emoji_usage: 'Minimal (0-1)',
    formatting: 'Full paragraphs, can be long',
    cta_style: 'Timestamp, pin comment, like to boost',
    best_practices: [
      'Can be detailed and long',
      'Reference timestamps',
      'Educational tone',
      'Pin valuable responses',
      'Link to related content'
    ]
  },

  facebook: {
    name: 'Facebook',
    max_length: 8000,
    recommended_length: '100-300 chars',
    tone: 'Warm, community-oriented, friendly',
    emoji_usage: 'Moderate (2-4)',
    formatting: '2-3 sentences or short paragraph',
    cta_style: 'Tag someone, react, encourage replies',
    best_practices: [
      'Community-focused language',
      'Encourage discussion',
      'Tag and mention others',
      'Warm and approachable',
      'Build connections'
    ]
  }
};

export const RESPONSE_TEMPLATES = {
  // LEAD SIGNAL RESPONSES (High buying intent)
  lead_signal: {
    linkedin: {
      template: "Great question, {name}! {answer_with_data}. Based on our work with {social_proof_number}+ businesses, {key_insight}. I'd be happy to walk you through how this would work for your specific situation. {cta}",
      example: "Great question, Sarah! The ROI typically shows within 30-60 days. Based on our work with 500+ gyms, those who implement this see an average 65% conversion rate (vs 30% industry avg). I'd be happy to walk you through how this would work for your gym. Feel free to book a quick 15-min call: [link] or DM me."
    },
    instagram: {
      template: "{enthusiasm_emoji} Love this question! {quick_answer} DM me and I'll send you {valuable_resource}! {cta_emoji}",
      example: "🔥 Love this question! Most gyms see results in 30-60 days. DM me and I'll send you the full case study! 👇💪"
    },
    twitter: {
      template: "{answer_core_point}. {proof_statement}. DM for details.",
      example: "30-60 days for most. We've tracked 500+ gyms—the data is wild. DM for the case study. 📊"
    }
  },

  // QUESTION RESPONSES (Genuine inquiry)
  question: {
    linkedin: {
      template: "{acknowledge_question}. {answer_clearly}. {optional_data_point}. {soft_cta}",
      example: "Excellent question! The system works by scoring leads 0-150 using 12 proven frameworks (SPIN, MEDDIC, BANT, etc). We've found this catches 95% of high-intent leads that traditional scoring misses. Happy to share more details if you're curious—feel free to connect or DM."
    },
    instagram: {
      template: "{emoji} {short_answer}! {one_liner_value_add}. {cta_if_interested}",
      example: "💡 It uses 12 sales frameworks to score leads! Way more accurate than traditional methods. Want the full breakdown? Link in bio! ✨"
    },
    twitter: {
      template: "{direct_answer}. {proof_or_insight}.",
      example: "12 sales frameworks (SPIN, MEDDIC, BANT, etc.). Catches 95% of high-intent leads traditional scoring misses."
    }
  },

  // COMPLIMENT RESPONSES (Positive feedback)
  compliment: {
    linkedin: {
      template: "Thank you, {name}! {acknowledge_specifically}. {share_credit_if_applicable}. {invite_to_engage}",
      example: "Thank you, John! Really appreciate you highlighting the conversion rate impact—that's the metric we obsess over. Our entire team works hard to make sure every feature drives real ROI. If you ever want to discuss lead gen strategies, always happy to connect!"
    },
    instagram: {
      template: "{gratitude_emoji} Thank you! {brief_acknowledgment}. {encourage_sharing} {emoji}",
      example: "🙏 Thank you! Comments like this fuel us! Tag someone who needs to see this! 💪✨"
    },
    twitter: {
      template: "🙏 {brief_thanks}. {optional_expansion}",
      example: "🙏 Appreciate this. Building in public means feedback like this keeps us going."
    }
  },

  // OBJECTION RESPONSES (Price, timing, skepticism)
  objection: {
    linkedin: {
      template: "{empathize_with_concern}. {reframe_with_value_equation}. {proof_point}. {offer_to_discuss}",
      example: "Totally understand the pricing concern, Sarah. The way we think about it: would you pay $400/month to generate an extra $612K/month in revenue? (That's the avg for our customers). Here's the ROI breakdown: [link]. Happy to walk through the numbers for your specific situation—DM or book a call."
    },
    instagram: {
      template: "{acknowledge_emoji} I get it! {quick_reframe}. {social_proof}. DM for the real numbers! {emoji}",
      example: "💯 I get it! But check this: $400/mo → $612K/mo avg revenue (real client data). DM for the breakdown! 📊"
    },
    twitter: {
      template: "{agree_with_concern}. {reframe_sharply}. {proof}.",
      example: "Fair question. $400/mo → $612K/mo revenue (avg client). That's 195x ROI. The data speaks for itself."
    }
  },

  // COMPLAINT RESPONSES (Negative experience)
  complaint: {
    linkedin: {
      template: "{apologize_sincerely}. {acknowledge_specific_issue}. {immediate_action_taken}. {invite_to_resolve_privately}",
      example: "I'm really sorry to hear about this experience, John. This isn't the level of service we pride ourselves on. I'm escalating this to our support lead immediately. Could you DM me your account details so I can personally make sure this is resolved today? I want to make this right."
    },
    instagram: {
      template: "{emoji} So sorry to hear this! {brief_acknowledgment}. DM me your details and I'll fix this ASAP! {emoji}",
      example: "😞 So sorry to hear this! That's not the experience we want for you. DM me your details and I'll fix this ASAP! 🙏"
    },
    twitter: {
      template: "Sorry to hear this. {acknowledge}. DM me your details—I'll get this resolved today.",
      example: "Sorry to hear this. That's not acceptable on our end. DM me your details—I'll get this resolved today."
    }
  },

  // ENGAGEMENT RESPONSES (Casual interaction)
  engagement: {
    linkedin: {
      template: "{acknowledge_positively}. {optional_expansion}. {light_cta}",
      example: "Glad this resonated with you! The data on lead conversion is fascinating when you dig into it. Let me know if you ever want to discuss strategies!"
    },
    instagram: {
      template: "{emoji_response} {brief_acknowledgment}! {optional_emoji}",
      example: "🔥🙌 Love the energy! 💪"
    },
    twitter: {
      template: "{brief_acknowledgment}",
      example: "🙌"
    }
  }
};

/**
 * Get platform-specific formatting guidelines
 */
export function getPlatformGuidelines(platform) {
  return PLATFORM_SPECS[platform.toLowerCase()] || PLATFORM_SPECS.linkedin;
}

/**
 * Get template for specific scenario and platform
 */
export function getResponseTemplate(intent, platform) {
  const intentKey = intent.toLowerCase().replace('_', '_');
  return RESPONSE_TEMPLATES[intentKey]?.[platform.toLowerCase()] || null;
}

/**
 * Format response according to platform rules
 */
export function formatResponseForPlatform(responseText, platform) {
  const guidelines = getPlatformGuidelines(platform);

  let formatted = responseText;

  // Truncate if exceeds max length
  if (formatted.length > guidelines.max_length) {
    formatted = formatted.substring(0, guidelines.max_length - 3) + '...';
  }

  return {
    text: formatted,
    length: formatted.length,
    within_guidelines: formatted.length <= guidelines.max_length,
    platform_notes: `${guidelines.name}: ${guidelines.recommended_length}, ${guidelines.emoji_usage} emojis, ${guidelines.tone}`
  };
}

/**
 * Validate response meets platform requirements
 */
export function validateResponse(responseText, platform, intent) {
  const guidelines = getPlatformGuidelines(platform);
  const validation = {
    valid: true,
    warnings: [],
    errors: []
  };

  // Length check
  if (responseText.length > guidelines.max_length) {
    validation.errors.push(`Response exceeds max length (${responseText.length} > ${guidelines.max_length})`);
    validation.valid = false;
  }

  // Emoji check
  const emojiCount = (responseText.match(/[\u{1F300}-\u{1F9FF}]/gu) || []).length;

  if (platform === 'linkedin' && emojiCount > 2) {
    validation.warnings.push(`Too many emojis for LinkedIn (${emojiCount}). Recommended: 0-2`);
  }

  if (platform === 'instagram' && emojiCount < 2) {
    validation.warnings.push(`Consider adding more emojis for Instagram (${emojiCount}). Recommended: 3-5`);
  }

  if (platform === 'tiktok' && emojiCount < 3) {
    validation.warnings.push(`Add more emojis for TikTok (${emojiCount}). Recommended: 5-8`);
  }

  // CTA check
  const hasCTA = /\b(DM|link|click|book|call|visit|check|see|read|watch|follow|subscribe|tag|share|save)\b/i.test(responseText);

  if (!hasCTA && intent === 'LEAD_SIGNAL') {
    validation.warnings.push('No clear CTA found for a lead signal response');
  }

  return validation;
}

/**
 * Suggest improvements for response
 */
export function suggestImprovements(responseText, platform, intent) {
  const suggestions = [];
  const guidelines = getPlatformGuidelines(platform);

  // Platform-specific suggestions
  if (platform === 'linkedin') {
    if (responseText.length < 100) {
      suggestions.push('LinkedIn audience values depth. Consider expanding to 200-500 chars.');
    }
    if (!responseText.match(/\d+/)) {
      suggestions.push('Add data/statistics for LinkedIn credibility');
    }
  }

  if (platform === 'instagram') {
    if (responseText.length > 150) {
      suggestions.push('Instagram responses work better when kept short (50-150 chars)');
    }
    if (!responseText.match(/[\u{1F300}-\u{1F9FF}]/gu)) {
      suggestions.push('Add 3-5 emojis for Instagram engagement');
    }
  }

  if (platform === 'twitter') {
    if (responseText.length > 200) {
      suggestions.push('Consider splitting into a thread or shortening for Twitter impact');
    }
    if (responseText.split('.').length > 3) {
      suggestions.push('Twitter works better with 1-2 punchy sentences');
    }
  }

  // Intent-specific suggestions
  if (intent === 'LEAD_SIGNAL') {
    if (!responseText.match(/\b(book|call|DM|schedule|calendar)\b/i)) {
      suggestions.push('Add clear CTA for lead conversion (book call, DM, etc.)');
    }
  }

  return suggestions;
}

export default {
  PLATFORM_SPECS,
  RESPONSE_TEMPLATES,
  getPlatformGuidelines,
  getResponseTemplate,
  formatResponseForPlatform,
  validateResponse,
  suggestImprovements
};

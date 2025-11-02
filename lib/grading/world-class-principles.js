/**
 * World-Class Sales & Marketing Principles Database
 * Based on $100M+ businesses and legendary marketers
 *
 * Sources:
 * - Alex Hormozi ($100M Offers, $100M Leads)
 * - Russell Brunson (ClickFunnels - $100M+/year)
 * - Eugene Schwartz (Breakthrough Advertising)
 * - Donald Miller (StoryBrand)
 * - Dan Kennedy (No B.S. Direct Marketing)
 * - Gary Halbert (The Boron Letters)
 * - Grant Cardone (10X Rule)
 * - David Ogilvy (Advertising legend)
 */

/**
 * COPYWRITING PRINCIPLES (Score: 0-100)
 */
export const COPYWRITING_PRINCIPLES = {
  // Alex Hormozi - Value Equation
  hormozi_value: {
    name: "Hormozi Value Equation",
    weight: 20,
    criteria: [
      {
        id: "dream_outcome",
        name: "Dream Outcome Clarity",
        description: "Does copy articulate the specific dream outcome?",
        perfect: "Specific, tangible, measurable outcome stated clearly",
        poor: "Vague benefits, no clear outcome",
        examples: {
          good: "Lose 20 lbs in 90 days without giving up your favorite foods",
          bad: "Get healthier and feel better"
        }
      },
      {
        id: "perceived_likelihood",
        name: "Perceived Likelihood of Success",
        description: "Does copy increase belief it will work?",
        perfect: "Social proof, data, guarantees, case studies",
        poor: "Just claims without proof",
        examples: {
          good: "1,247 members lost average 23 lbs (see their transformations)",
          bad: "Our program works great!"
        }
      },
      {
        id: "time_delay",
        name: "Time Delay Reduction",
        description: "Does copy show speed to results?",
        perfect: "Specific timeline, quick wins emphasized",
        poor: "No mention of how long",
        examples: {
          good: "See results in first 7 days, transform in 90",
          bad: "Results take time but you'll get there"
        }
      },
      {
        id: "effort_sacrifice",
        name: "Effort & Sacrifice Minimization",
        description: "Does copy reduce perceived effort?",
        perfect: "Simple, easy, no sacrifice positioning",
        poor: "Sounds hard, time-consuming, painful",
        examples: {
          good: "3 workouts/week, 45 minutes each, eat what you love",
          bad: "Requires complete lifestyle overhaul and daily 2-hour commitment"
        }
      }
    ]
  },

  // Russell Brunson - Hook, Story, Offer
  brunson_framework: {
    name: "Brunson Hook-Story-Offer",
    weight: 15,
    criteria: [
      {
        id: "hook_attention",
        name: "Hook Grabs Attention",
        description: "First line stops the scroll",
        perfect: "Pattern interrupt, curiosity, bold claim, question",
        poor: "Generic greeting, corporate speak",
        examples: {
          good: "Why are 78% of gym members wasting their money?",
          bad: "Dear valued customer, we hope this email finds you well"
        }
      },
      {
        id: "story_relatability",
        name: "Story Creates Connection",
        description: "Story makes prospect see themselves",
        perfect: "Relatable character, clear transformation, emotional",
        poor: "No story, or story about you not them",
        examples: {
          good: "Sarah was skeptical too. Tried 5 gyms, gained weight each time...",
          bad: "We've been in business since 2010 and have great equipment"
        }
      },
      {
        id: "offer_clarity",
        name: "Offer is Crystal Clear",
        description: "Exactly what they get and how to get it",
        perfect: "Specific offer, clear CTA, easy next step",
        poor: "Vague, confusing, no clear action",
        examples: {
          good: "Book your free assessment (reply YES or call 817-555-0100)",
          bad: "Learn more about our various membership options"
        }
      }
    ]
  },

  // Eugene Schwartz - 5 Levels of Awareness
  schwartz_awareness: {
    name: "Schwartz 5 Awareness Levels",
    weight: 15,
    criteria: [
      {
        id: "awareness_match",
        name: "Copy Matches Awareness Level",
        description: "Message appropriate for where prospect is",
        perfect: "Matches exact awareness stage of lead",
        poor: "Pitching Most Aware copy to Unaware prospect",
        scoring: {
          most_aware: "Ready to buy, just needs mechanism (you)",
          product_aware: "Knows you exist, needs differentiation",
          solution_aware: "Knows solution exists, needs your product",
          problem_aware: "Knows problem, needs solution education",
          unaware: "Doesn't know problem exists, needs awakening"
        }
      },
      {
        id: "sophistication_level",
        name: "Market Sophistication Addressed",
        description: "Accounts for how many similar offers they've seen",
        perfect: "Novel mechanism or unique angle",
        poor: "Same pitch everyone uses",
        examples: {
          good: "Not another HIIT class - this is metabolic resistance training",
          bad: "We offer personal training and group classes"
        }
      }
    ]
  },

  // Donald Miller - StoryBrand 7 Framework
  miller_storybrand: {
    name: "Miller StoryBrand Framework",
    weight: 15,
    criteria: [
      {
        id: "hero_positioning",
        name: "Customer is Hero (Not You)",
        description: "Prospect positioned as hero, you as guide",
        perfect: "All about them and their journey",
        poor: "All about you and your accomplishments",
        examples: {
          good: "Your fitness journey, we're here to guide you",
          bad: "We're the #1 gym with 50 trainers and awards"
        }
      },
      {
        id: "problem_identification",
        name: "Clear Problem Identified",
        description: "External + Internal + Philosophical problem",
        perfect: "All 3 problem levels addressed",
        poor: "Only surface problem mentioned",
        examples: {
          good: "Can't lose weight (external), feel hopeless (internal), deserve better (philosophical)",
          bad: "Need to exercise more"
        }
      },
      {
        id: "plan_clarity",
        name: "Simple Plan Provided",
        description: "3-step plan to success",
        perfect: "Clear 3-step process, easy to understand",
        poor: "Overwhelming or no plan given",
        examples: {
          good: "1. Book assessment 2. Get custom plan 3. Start winning",
          bad: "Contact us and we'll figure something out"
        }
      },
      {
        id: "call_to_action",
        name: "Clear Call to Action",
        description: "One direct + one transitional CTA",
        perfect: "Direct CTA (book now) + Transitional (learn more)",
        poor: "No CTA or too many options",
        examples: {
          good: "Book free assessment (direct) or download success guide (transitional)",
          bad: "Visit our website, follow us, call us, or email us maybe"
        }
      }
    ]
  },

  // Dan Kennedy - Direct Response
  kennedy_direct_response: {
    name: "Kennedy Direct Response",
    weight: 15,
    criteria: [
      {
        id: "urgency_scarcity",
        name: "Urgency & Scarcity Present",
        description: "Reason to act NOW",
        perfect: "Genuine deadline, limited spots, price increase",
        poor: "No urgency, can act anytime",
        examples: {
          good: "Only 3 spots left this month. New rates start Dec 1st.",
          bad: "Join whenever you're ready"
        }
      },
      {
        id: "risk_reversal",
        name: "Risk Reversal (Guarantee)",
        description: "All risk on you, none on them",
        perfect: "Strong guarantee, trial period, money-back",
        poor: "No guarantee or weak guarantee",
        examples: {
          good: "30-day trial. Not happy? Full refund, no questions asked.",
          bad: "All sales final, no refunds"
        }
      },
      {
        id: "specificity",
        name: "Specificity vs Generality",
        description: "Specific numbers, details, facts",
        perfect: "Specific numbers, dates, quantities, names",
        poor: "Vague, general claims",
        examples: {
          good: "Average client loses 23.4 lbs in first 90 days",
          bad: "Clients lose lots of weight"
        }
      }
    ]
  },

  // Gary Halbert - Emotional Triggers
  halbert_emotion: {
    name: "Halbert Emotional Triggers",
    weight: 10,
    criteria: [
      {
        id: "curiosity",
        name: "Curiosity Gap Created",
        description: "Makes them want to know more",
        perfect: "Open loop, unanswered question, mystery",
        poor: "Tells everything, no intrigue",
        examples: {
          good: "The one exercise that torches belly fat (it's not cardio)",
          bad: "Do squats and planks for your core"
        }
      },
      {
        id: "fear_of_loss",
        name: "Loss Aversion Triggered",
        description: "What they lose by NOT acting",
        perfect: "Clear cost of inaction shown",
        poor: "Only shows gains, no loss",
        examples: {
          good: "Every day you wait, you lose 1% muscle mass after 40",
          bad: "Join and you'll feel great"
        }
      }
    ]
  },

  // David Ogilvy - Advertising Principles
  ogilvy_principles: {
    name: "Ogilvy Advertising Principles",
    weight: 10,
    criteria: [
      {
        id: "headline_power",
        name: "Headline Sells",
        description: "80% of success is headline",
        perfect: "Benefit-driven, specific, compelling",
        poor: "Clever wordplay, vague, no benefit",
        examples: {
          good: "Lose 20 Pounds in 90 Days Without Giving Up Carbs",
          bad: "Where Fitness Meets Fun"
        }
      },
      {
        id: "brand_consistency",
        name: "Brand Voice Consistency",
        description: "Consistent personality throughout",
        perfect: "Same tone, style, personality every touch",
        poor: "Tone shifts randomly",
        check: "Does every message sound like same person?"
      }
    ]
  }
};

/**
 * SALES PROCESS PRINCIPLES (Score: 0-100)
 */
export const SALES_PROCESS_PRINCIPLES = {
  // Response Time
  response_speed: {
    name: "Response Speed (Harvard Study)",
    weight: 20,
    criteria: [
      {
        id: "first_response",
        name: "First Response Time",
        description: "Speed to first contact after lead comes in",
        grading: {
          A: "< 5 minutes (60x more likely to qualify)",
          B: "5-10 minutes (30x more likely)",
          C: "10-30 minutes (10x more likely)",
          D: "30-60 minutes (5x more likely)",
          F: "> 1 hour (baseline)"
        },
        source: "Harvard Business Review - Lead Response Study"
      }
    ]
  },

  // Follow-Up Persistence
  followup_persistence: {
    name: "Follow-Up Persistence",
    weight: 20,
    criteria: [
      {
        id: "touch_count",
        name: "Number of Touches",
        description: "How many times you follow up",
        grading: {
          A: "12-14 touches (80% of sales happen after 5th touch)",
          B: "8-11 touches",
          C: "5-7 touches",
          D: "3-4 touches",
          F: "1-2 touches (where most businesses stop)"
        },
        source: "National Sales Executive Association"
      },
      {
        id: "touch_variety",
        name: "Channel Variety",
        description: "How many channels used",
        grading: {
          A: "4+ channels (email, phone, SMS, LinkedIn, mail)",
          B: "3 channels",
          C: "2 channels",
          D: "1 channel",
          F: "Inconsistent or no follow-up"
        }
      }
    ]
  },

  // Qualification
  lead_qualification: {
    name: "Lead Qualification (BANT/MEDDIC)",
    weight: 15,
    criteria: [
      {
        id: "budget_check",
        name: "Budget Qualification",
        description: "Can they afford it?",
        check: "Asked about budget or priced them out early"
      },
      {
        id: "authority_check",
        name: "Authority Qualification",
        description: "Decision maker identified?",
        check: "Confirmed who makes the decision"
      },
      {
        id: "need_check",
        name: "Need Identification",
        description: "Real pain point uncovered?",
        check: "Discovered actual problem, not assumed"
      },
      {
        id: "timing_check",
        name: "Timeline Established",
        description: "When do they need to start?",
        check: "Specific date or urgency confirmed"
      }
    ]
  },

  // Objection Handling
  objection_handling: {
    name: "Objection Handling",
    weight: 15,
    criteria: [
      {
        id: "price_objection",
        name: "Price Objection Handled",
        description: "How price concerns addressed",
        perfect: "Reframe to value, break down cost, show ROI",
        poor: "Drop price or avoid topic",
        examples: {
          good: "$200/month = $6.67/day for your health. Less than your daily coffee.",
          bad: "Well, we can give you a discount..."
        }
      },
      {
        id: "time_objection",
        name: "Time Objection Handled",
        description: "How time concerns addressed",
        perfect: "Show time efficiency, quick wins, flexible schedule",
        poor: "Agree it takes time or push harder",
        examples: {
          good: "3x per week, 45 min. Less time than your commute.",
          bad: "Yeah it's a commitment but worth it"
        }
      }
    ]
  },

  // Close Technique
  closing: {
    name: "Closing Techniques",
    weight: 15,
    criteria: [
      {
        id: "assumptive_close",
        name: "Assumptive Language",
        description: "Assumes they're buying",
        examples: {
          good: "When you start next week, which time works better - morning or evening?",
          bad: "So... do you want to sign up or...?"
        }
      },
      {
        id: "alternative_close",
        name: "Alternative Choice Close",
        description: "Both options lead to yes",
        examples: {
          good: "Would you prefer Monday/Wednesday or Tuesday/Thursday?",
          bad: "Do you want to join?"
        }
      }
    ]
  },

  // Relationship Building
  relationship_building: {
    name: "Relationship Building",
    weight: 15,
    criteria: [
      {
        id: "personalization",
        name: "Personal Connection",
        description: "Human, personal touches",
        perfect: "References their details, remembers conversations, personal notes",
        poor: "Generic, robotic, no personal touch",
        check: "Would they know this is from a human who knows them?"
      },
      {
        id: "value_first",
        name: "Value Before Ask",
        description: "Give before you get",
        perfect: "Free value, insights, help before asking for sale",
        poor: "Only reach out to ask for money",
        examples: {
          good: "Here's your free workout plan + nutrition guide. No strings.",
          bad: "Ready to buy yet?"
        }
      }
    ]
  }
};

/**
 * REPUTATION & TRUST PRINCIPLES (Score: 0-100)
 */
export const REPUTATION_PRINCIPLES = {
  // Social Proof
  social_proof: {
    name: "Social Proof (Cialdini)",
    weight: 30,
    criteria: [
      {
        id: "review_quantity",
        name: "Review Quantity",
        description: "Number of reviews",
        grading: {
          A: "200+ reviews",
          B: "100-199 reviews",
          C: "50-99 reviews",
          D: "20-49 reviews",
          F: "< 20 reviews"
        }
      },
      {
        id: "review_quality",
        name: "Average Rating",
        description: "Star rating",
        grading: {
          A: "4.8-5.0 stars",
          B: "4.5-4.7 stars",
          C: "4.0-4.4 stars",
          D: "3.5-3.9 stars",
          F: "< 3.5 stars"
        }
      },
      {
        id: "review_recency",
        name: "Review Recency",
        description: "How recent are reviews",
        grading: {
          A: "10+ reviews in last 30 days",
          B: "5-9 reviews in last 30 days",
          C: "2-4 reviews in last 30 days",
          D: "1 review in last 30 days",
          F: "No reviews in last 30 days"
        }
      },
      {
        id: "response_rate",
        name: "Response Rate",
        description: "% of reviews responded to",
        grading: {
          A: "95-100% response rate",
          B: "80-94% response rate",
          C: "60-79% response rate",
          D: "40-59% response rate",
          F: "< 40% response rate"
        }
      }
    ]
  },

  // Trust Signals
  trust_signals: {
    name: "Trust & Authority Signals",
    weight: 25,
    criteria: [
      {
        id: "guarantee_strength",
        name: "Guarantee Strength",
        description: "How strong is your guarantee?",
        grading: {
          A: "Strong guarantee (30-90 day, money-back, no questions)",
          B: "Good guarantee (trial period or conditional refund)",
          C: "Weak guarantee (partial refund or strict conditions)",
          D: "No guarantee but some flexibility",
          F: "No guarantee, all sales final"
        }
      },
      {
        id: "credentials_shown",
        name: "Credentials & Proof",
        description: "Authority markers present",
        perfect: "Certifications, years in business, client count, awards",
        poor: "No proof of expertise",
        check: "Can prospect verify your expertise?"
      }
    ]
  },

  // Negative Review Management
  negative_review_handling: {
    name: "Negative Review Handling",
    weight: 25,
    criteria: [
      {
        id: "response_time_negative",
        name: "Response Time to Negative Reviews",
        description: "How fast do you respond to 1-3 star reviews?",
        grading: {
          A: "< 4 hours",
          B: "4-12 hours",
          C: "12-24 hours",
          D: "24-48 hours",
          F: "> 48 hours or no response"
        }
      },
      {
        id: "response_quality",
        name: "Response Quality",
        description: "How good is the response?",
        perfect: "Apologize, acknowledge, offer solution, take offline",
        poor: "Defensive, blame customer, generic",
        examples: {
          good: "I'm so sorry, Sarah. This isn't acceptable. Please call me directly at [number] so I can make this right.",
          bad: "We're sorry you feel that way. We have policies for a reason."
        }
      }
    ]
  },

  // Review Acquisition
  review_acquisition: {
    name: "Review Acquisition Strategy",
    weight: 20,
    criteria: [
      {
        id: "request_timing",
        name: "Review Request Timing",
        description: "When do you ask for reviews?",
        perfect: "Right after positive moment/milestone",
        poor: "Random timing or never ask",
        examples: {
          good: "Ask immediately after compliment or goal achieved",
          bad: "Mass email to all customers annually"
        }
      },
      {
        id: "request_method",
        name: "Review Request Method",
        description: "How do you ask?",
        perfect: "Personal SMS/message with direct link, easy 1-click",
        poor: "Generic email, hard to find review page",
        examples: {
          good: "SMS: 'Hey John! Congrats on your goal! Mind leaving us a quick review? [link]'",
          bad: "Email: 'Dear customer, please consider leaving us a review on our website if you have time.'"
        }
      }
    ]
  }
};

/**
 * CONVERSION OPTIMIZATION PRINCIPLES (Score: 0-100)
 */
export const CONVERSION_PRINCIPLES = {
  // Landing Page
  landing_page: {
    name: "Landing Page Optimization",
    weight: 25,
    criteria: [
      {
        id: "above_fold_clarity",
        name: "Above-the-Fold Clarity",
        description: "Clear value prop in 3 seconds",
        perfect: "One sentence explains exactly what you do and for who",
        poor: "Vague, clever, or takes scrolling to understand",
        examples: {
          good: "MetroFlex: Weight Loss for Busy Professionals (Fort Worth)",
          bad: "Welcome to MetroFlex: Where Fitness Meets Excellence"
        }
      },
      {
        id: "friction_reduction",
        name: "Friction Reduction",
        description: "How easy is it to convert?",
        grading: {
          A: "1-click (phone, calendar, chatbot)",
          B: "Short form (3-5 fields)",
          C: "Medium form (6-10 fields)",
          D: "Long form (10+ fields)",
          F: "No clear CTA or broken form"
        }
      }
    ]
  },

  // Lead Magnet
  lead_magnet: {
    name: "Lead Magnet Quality",
    weight: 25,
    criteria: [
      {
        id: "value_perception",
        name: "Perceived Value",
        description: "Does it feel like it should cost money?",
        perfect: "Could charge $97+ for this",
        poor: "Generic PDF or low-value",
        examples: {
          good: "Custom workout plan + meal prep guide + video tutorials",
          bad: "Generic '10 fitness tips' PDF"
        }
      },
      {
        id: "quick_win",
        name: "Quick Win Included",
        description: "Can they get result immediately?",
        perfect: "One thing they can do today for instant result",
        poor: "All theory, no immediate action",
        examples: {
          good: "5-minute morning routine that burns fat all day",
          bad: "Comprehensive guide to exercise science"
        }
      }
    ]
  },

  // Email Deliverability
  deliverability: {
    name: "Email Deliverability",
    weight: 20,
    criteria: [
      {
        id: "spam_score",
        name: "Spam Score",
        description: "Likelihood to hit spam",
        grading: {
          A: "< 2 spam score",
          B: "2-3 spam score",
          C: "3-5 spam score",
          D: "5-7 spam score",
          F: "> 7 spam score (will hit spam)"
        }
      },
      {
        id: "technical_setup",
        name: "Technical Setup",
        description: "SPF, DKIM, DMARC configured?",
        check: "All 3 authentication protocols properly set up"
      }
    ]
  },

  // A/B Testing
  testing_culture: {
    name: "Testing & Iteration",
    weight: 15,
    criteria: [
      {
        id: "active_tests",
        name: "Active Tests Running",
        description: "Are you testing continuously?",
        grading: {
          A: "Always testing (2-3 active tests)",
          B: "Regular testing (monthly tests)",
          C: "Occasional testing (quarterly)",
          D: "Rare testing (annual)",
          F: "No testing (set it and forget it)"
        }
      }
    ]
  },

  // Retargeting
  retargeting: {
    name: "Retargeting Strategy",
    weight: 15,
    criteria: [
      {
        id: "pixel_installed",
        name: "Tracking Pixels Installed",
        description: "Facebook, Google, LinkedIn pixels active?",
        check: "At least 1 retargeting pixel active"
      },
      {
        id: "retargeting_active",
        name: "Retargeting Campaigns Active",
        description: "Running retargeting ads?",
        check: "Active campaigns to website visitors"
      }
    ]
  }
};

/**
 * Calculate overall grade based on weighted scores
 */
export function calculateOverallGrade(scores) {
  const categoryGrades = {
    copywriting: scores.copywriting || 0,
    sales_process: scores.sales_process || 0,
    reputation: scores.reputation || 0,
    conversion: scores.conversion || 0
  };

  // Weight distribution
  const weights = {
    copywriting: 0.30,      // 30% - Words sell
    sales_process: 0.30,    // 30% - Process converts
    reputation: 0.25,       // 25% - Trust matters
    conversion: 0.15        // 15% - Optimization
  };

  const overall =
    (categoryGrades.copywriting * weights.copywriting) +
    (categoryGrades.sales_process * weights.sales_process) +
    (categoryGrades.reputation * weights.reputation) +
    (categoryGrades.conversion * weights.conversion);

  return {
    overall: Math.round(overall),
    breakdown: categoryGrades,
    letterGrade: getLetterGrade(overall),
    capability: getCapabilityLevel(overall)
  };
}

function getLetterGrade(score) {
  if (score >= 95) return 'A+';
  if (score >= 90) return 'A';
  if (score >= 85) return 'A-';
  if (score >= 80) return 'B+';
  if (score >= 75) return 'B';
  if (score >= 70) return 'B-';
  if (score >= 65) return 'C+';
  if (score >= 60) return 'C';
  if (score >= 55) return 'C-';
  if (score >= 50) return 'D';
  return 'F';
}

function getCapabilityLevel(score) {
  if (score >= 95) return '$10M+/month - Elite tier (top 0.1%)';
  if (score >= 90) return '$5M-10M/month - World-class (top 1%)';
  if (score >= 85) return '$2M-5M/month - Exceptional (top 5%)';
  if (score >= 80) return '$1M-2M/month - Excellent (top 10%)';
  if (score >= 75) return '$500K-1M/month - Very good (top 20%)';
  if (score >= 70) return '$250K-500K/month - Good (top 30%)';
  if (score >= 60) return '$100K-250K/month - Above average';
  if (score >= 50) return '$50K-100K/month - Average';
  return 'Below $50K/month - Needs significant improvement';
}

export default {
  COPYWRITING_PRINCIPLES,
  SALES_PROCESS_PRINCIPLES,
  REPUTATION_PRINCIPLES,
  CONVERSION_PRINCIPLES,
  calculateOverallGrade
};

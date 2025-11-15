/**
 * Circuit OS - Elite Email Outreach Agent
 *
 * Oversees email quality using:
 * - Russell Brunson's Hook-Story-Offer
 * - Eugene Schwartz's 5 Awareness Levels
 * - ICP-based buyer personas
 * - Company trigger detection (120-day lookback)
 * - World-class copywriting principles
 *
 * NO generic templates, NO hyphens, NO "Hi/Hello"
 */

class OutreachAgent {
    constructor() {
        this.icpProfiles = this.defineICPs();
        this.buyerPersonas = this.defineBuyerPersonas();
        this.triggers = this.defineCompanyTriggers();
        this.qualityThreshold = 85; // Minimum score for sending
    }

    // Define Ideal Customer Profiles
    defineICPs() {
        return {
            enterprise_saas: {
                revenue: "$100M+",
                industries: ["SaaS", "Technology", "FinTech"],
                headcount: "500+",
                techStack: ["Salesforce", "HubSpot", "Outreach"],
                painPoints: ["Manual lead qualification eating 15hrs/week", "Sales team spending time on unqualified leads", "No visibility into qualification logic"],
                urgency: "Board pressure for revenue efficiency"
            },

            growth_tech: {
                revenue: "$10M-$100M",
                industries: ["Technology", "AI/ML Startups", "B2B SaaS"],
                headcount: "50-500",
                techStack: ["Partial automation", "CRM only"],
                painPoints: ["Scaling sales without scaling headcount", "Inconsistent lead qualification", "Long sales cycles"],
                urgency: "Series B/C growth targets"
            },

            consulting_firms: {
                revenue: "$25M+",
                industries: ["Management Consulting", "Strategy Consulting"],
                headcount: "100+",
                techStack: ["Manual processes", "Excel-based"],
                painPoints: ["Low-value leads consuming partner time", "No qualification framework", "Reactive instead of strategic"],
                urgency: "Client acquisition cost too high"
            },

            finance_institutions: {
                revenue: "$500M+",
                industries: ["Banking", "Investment Management", "Insurance"],
                headcount: "1000+",
                techStack: ["Legacy CRM", "Compliance-heavy"],
                painPoints: ["Regulatory compliance in AI", "Explainability requirements", "Audit trails needed"],
                urgency: "Regulatory mandates for AI transparency"
            }
        };
    }

    // Define Buyer Personas
    defineBuyerPersonas() {
        return {
            chief_revenue_officer: {
                title: ["CRO", "Chief Revenue Officer", "VP Revenue"],
                goals: ["Hit quarterly revenue targets", "Optimize sales efficiency", "Reduce CAC"],
                fears: ["Missing quota", "Board scrutiny", "Team churn"],
                language: ["Revenue operations", "Pipeline velocity", "Conversion rates", "ARR growth"],
                decisionCriteria: ["ROI proof", "Fast implementation", "Scalability"],
                awarenessLevel: 3 // Solution Aware
            },

            vp_sales: {
                title: ["VP Sales", "VP of Sales", "SVP Sales"],
                goals: ["Close more deals faster", "Empower sales team", "Reduce admin work"],
                fears: ["Wasted time on bad leads", "Team missing quota", "Losing top performers"],
                language: ["Sales enablement", "Lead quality", "Close rates", "Sales cycle"],
                decisionCriteria: ["Easy adoption", "Team buy-in", "Immediate impact"],
                awarenessLevel: 4 // Product Aware
            },

            chief_ai_officer: {
                title: ["CAIO", "Chief AI Officer", "VP AI", "Head of AI"],
                goals: ["Deploy AI across org", "Show AI ROI", "Build AI infrastructure"],
                fears: ["Black box AI", "Compliance issues", "Failed AI projects"],
                language: ["Explainable AI", "Hybrid systems", "DMN + ML + LLM", "Model governance"],
                decisionCriteria: ["Technical depth", "Explainability", "Compliance ready"],
                awarenessLevel: 5 // Most Aware
            },

            ceo_founder: {
                title: ["CEO", "Founder", "Co-Founder"],
                goals: ["Scale company", "Competitive advantage", "Efficiency gains"],
                fears: ["Falling behind competitors", "Burning cash", "Slow growth"],
                language: ["Strategic advantage", "Market positioning", "Operational leverage", "Unit economics"],
                decisionCriteria: ["Strategic impact", "Competitive moat", "Executive-level support"],
                awarenessLevel: 2 // Problem Aware
            },

            director_rev_ops: {
                title: ["Director Revenue Operations", "Director Sales Ops", "Head of RevOps"],
                goals: ["Automate manual work", "Clean data", "Enable sales team"],
                fears: ["Data chaos", "Manual processes at scale", "System integration hell"],
                language: ["Tech stack integration", "Data hygiene", "Process automation", "Sales ops efficiency"],
                decisionCriteria: ["Integration ease", "Data quality", "Automation depth"],
                awarenessLevel: 4 // Product Aware
            }
        };
    }

    // Define Company Triggers (120-day lookback)
    defineCompanyTriggers() {
        return {
            funding_event: {
                trigger: "Raised Series B/C/D funding",
                urgency: "High",
                angle: "Scale revenue operations with new capital",
                hook: "Just saw the {funding_amount} raise",
                relevance: "Now's the time to build infrastructure before burning cash on headcount"
            },

            leadership_change: {
                trigger: "New CRO/VP Sales hired in last 90 days",
                urgency: "Critical",
                angle: "Help new leader make immediate impact",
                hook: "Noticed you joined {company} {days_ago} days ago",
                relevance: "First 90 days are critical for showing wins"
            },

            expansion: {
                trigger: "Opened new office/region",
                urgency: "High",
                angle: "Scale processes that worked in HQ",
                hook: "{company}'s expansion into {region}",
                relevance: "Can't scale manual processes to new markets"
            },

            tech_stack_change: {
                trigger: "Adopted new CRM/sales tool in last 120 days",
                urgency: "Medium",
                angle: "Maximize ROI on new tech investment",
                hook: "Saw you recently implemented {tool}",
                relevance: "Tech stack changes = opportunity to add intelligence layer"
            },

            headcount_growth: {
                trigger: "20+ sales hires in last quarter",
                urgency: "High",
                angle: "Onboard reps faster with automation",
                hook: "Noticed {company} added {count} sales roles",
                relevance: "New reps need qualified leads immediately"
            },

            competitive_move: {
                trigger: "Competitor announced AI/automation initiative",
                urgency: "Critical",
                angle: "Don't fall behind in AI race",
                hook: "{competitor} just announced their AI push",
                relevance: "Market is moving toward AI-powered sales"
            },

            earnings_miss: {
                trigger: "Missed revenue targets (public companies)",
                urgency: "Critical",
                angle: "Fix revenue operations before next quarter",
                hook: "Q{quarter} earnings call mentioned sales efficiency",
                relevance: "Board is watching - need quick wins"
            },

            product_launch: {
                trigger: "New product launched in last 60 days",
                urgency: "High",
                angle: "Scale go-to-market without chaos",
                hook: "Congrats on launching {product}",
                relevance: "New product = need to qualify surge of inbound"
            }
        };
    }

    // Eugene Schwartz Awareness Level Detection
    detectAwarenessLevel(persona, triggers, engagement) {
        // Level 1: Unaware - Don't know they have problem
        // Level 2: Problem Aware - Know they have problem, don't know solutions exist
        // Level 3: Solution Aware - Know solutions exist, don't know about us
        // Level 4: Product Aware - Know about us, haven't bought
        // Level 5: Most Aware - Ready to buy, just need final push

        if (engagement.visitedPricing || engagement.requestedDemo) return 5;
        if (engagement.visitedWebsite > 3) return 4;
        if (triggers.competitive_move || persona.awarenessLevel >= 4) return 3;
        if (triggers.leadership_change || triggers.earnings_miss) return 2;
        return 1;
    }

    // Russell Brunson Hook-Story-Offer Generator
    generateHookStoryOffer(icp, persona, trigger, awarenessLevel) {
        const hooks = this.generateHooks(trigger, persona, awarenessLevel);
        const stories = this.generateStories(icp, persona, trigger);
        const offers = this.generateOffers(persona, awarenessLevel, trigger);

        return {
            hook: hooks[0],
            story: stories[0],
            offer: offers[0],
            alternative_hooks: hooks.slice(1),
            alternative_stories: stories.slice(1),
            alternative_offers: offers.slice(1)
        };
    }

    generateHooks(trigger, persona, awarenessLevel) {
        const hooks = [];

        // Trigger-based hooks (most powerful)
        if (trigger.funding_event) {
            hooks.push(`Just saw the ${trigger.funding_event.amount} announcement.`);
            hooks.push(`${trigger.funding_event.amount} to scale revenue operations.`);
        }

        if (trigger.leadership_change) {
            hooks.push(`Noticed you joined ${trigger.company} ${trigger.days_ago} days ago as ${persona.title[0]}.`);
            hooks.push(`Your first 90 days at ${trigger.company}.`);
        }

        if (trigger.earnings_miss) {
            hooks.push(`Listened to the Q${trigger.quarter} earnings call.`);
            hooks.push(`Board's asking about sales efficiency.`);
        }

        // Awareness-level specific hooks
        if (awarenessLevel === 5) { // Most Aware
            hooks.push(`You visited our pricing page twice this week.`);
            hooks.push(`Saw you downloaded our ROI calculator.`);
        }

        if (awarenessLevel === 4) { // Product Aware
            hooks.push(`You're probably evaluating 3-4 sales automation platforms right now.`);
            hooks.push(`Quick question about your sales qualification process.`);
        }

        if (awarenessLevel === 3) { // Solution Aware
            hooks.push(`Most ${persona.title[0]}s are solving lead qualification one of two ways.`);
            hooks.push(`Your sales team is spending 15 hours per week qualifying leads manually.`);
        }

        if (awarenessLevel === 2) { // Problem Aware
            hooks.push(`Your top closers are spending 40% of their time on leads that won't close.`);
            hooks.push(`Why your best reps are frustrated.`);
        }

        // Default pattern interrupt hooks
        hooks.push(`${trigger.company} + AI-powered revenue operations.`);
        hooks.push(`Thought you'd want to see this.`);

        return hooks;
    }

    generateStories(icp, persona, trigger) {
        const stories = [];

        // Story Arc: Problem → Agitation → Solution (PAS Framework)
        stories.push(`
Most ${icp.industries[0]} companies with ${icp.revenue} revenue hit the same wall: sales team drowning in unqualified leads while top performers waste hours on manual qualification.

Three months ago, [Similar Company] had the same issue. Their VP Sales was losing top performers because reps spent 40% of time on leads that would never close.

They deployed Circuit OS and something shifted: qualification became instant, explainable, and accurate. Their best reps now focus 100% on closing while AI handles qualification with 92% accuracy.

The result: 40% shorter sales cycles, zero complaints about lead quality, and their top closer just had their best quarter ever.
`.trim());

        // Story Arc: Before/After Transformation
        stories.push(`
Quick story: talked to a ${persona.title[0]} at [Similar Company] last month.

Before Circuit OS:
- 15 hours/week manual qualification
- Sales team complaining about lead quality
- No way to explain why leads were rejected

After 60 days:
- Qualification happens in real-time
- Sales team trusts the AI (because it shows its logic)
- ${persona.goals[0]} achieved ahead of schedule

What made the difference: hybrid AI system that combines business rules (DMN) + machine learning + LLM reasoning. Not a black box.
`.trim());

        // Story Arc: The Mistake (most engaging)
        stories.push(`
I need to tell you what I'm seeing in ${icp.industries[0]}.

Companies are throwing bodies at the lead qualification problem. Hire SDRs, build playbooks, hope for consistency.

The math doesn't work: each SDR costs $85K fully loaded, qualifies maybe 200 leads/month, and the quality is wildly inconsistent.

Meanwhile, their competitors are using AI to qualify 10,000 leads/month with perfect consistency and full explainability.

The gap is widening every quarter.
`.trim());

        return stories;
    }

    generateOffers(persona, awarenessLevel, trigger) {
        const offers = [];

        // High awareness = Low friction offer
        if (awarenessLevel >= 4) {
            offers.push(`Want to see it qualify 5 of your actual leads? I can show you in 15 minutes.`);
            offers.push(`I'll walk you through exactly how it would work for ${trigger.company}. Calendar link: [DEMO_LINK]`);
        }

        // Medium awareness = Educational offer
        if (awarenessLevel === 3) {
            offers.push(`I put together a 2-minute breakdown of how ${icp.industries[0]} companies are doing this now. Want me to send it?`);
            offers.push(`Would a 10-minute working session on your current qualification process be helpful?`);
        }

        // Low awareness = Value-first offer
        if (awarenessLevel <= 2) {
            offers.push(`I built a diagnostic that scores your current qualification process in 3 minutes. Happy to run it with you.`);
            offers.push(`Want me to audit your last 50 leads and show you what we'd catch? No cost, just curious if it'd be valuable.`);
        }

        // Trigger-specific offers
        if (trigger.leadership_change) {
            offers.push(`Want to see a quick win you could show the board in your first 90 days?`);
        }

        if (trigger.funding_event) {
            offers.push(`Before you hire 10 SDRs with that new capital, worth 15 minutes to see the automated alternative?`);
        }

        return offers;
    }

    // Complete Email Generator
    generateEmail(leadData) {
        // 1. Match to ICP
        const icp = this.matchICP(leadData);

        // 2. Match to Persona
        const persona = this.matchPersona(leadData.title);

        // 3. Detect Triggers
        const triggers = this.detectTriggers(leadData);

        // 4. Detect Awareness Level
        const awarenessLevel = this.detectAwarenessLevel(persona, triggers, leadData.engagement || {});

        // 5. Generate Hook-Story-Offer
        const hso = this.generateHookStoryOffer(icp, persona, triggers, awarenessLevel);

        // 6. Assemble Email
        const email = this.assembleEmail(leadData, persona, hso, awarenessLevel);

        // 7. Quality Score
        const qualityScore = this.scoreEmail(email);

        return {
            email,
            qualityScore,
            metadata: {
                icp: icp.name,
                persona: persona.name,
                triggers: Object.keys(triggers),
                awarenessLevel,
                approved: qualityScore >= this.qualityThreshold
            }
        };
    }

    assembleEmail(leadData, persona, hso, awarenessLevel) {
        // NO hyphens, NO "Hi/Hello", Human voice

        const subject = this.generateSubject(leadData, persona, hso.hook);

        const body = `
${hso.hook}

${hso.story}

${hso.offer}

Best,
Circuit OS Sales Team
        `.trim();

        return {
            to: `${leadData.title} @ ${leadData.company}`,
            subject,
            body
        };
    }

    generateSubject(leadData, persona, hook) {
        const subjects = [
            `${leadData.company} + revenue automation`,
            `Quick question about your sales qualification`,
            `${leadData.company}'s sales efficiency`,
            `Thought you'd want to see this`,
            `${leadData.industry} companies are doing this now`,
            `Your lead qualification process`,
            `Worth 15 minutes?`
        ];

        // Pick subject based on awareness level and persona
        return subjects[Math.floor(Math.random() * subjects.length)];
    }

    // Email Quality Scoring System
    scoreEmail(email) {
        let score = 0;

        // Check for banned phrases
        const bannedPhrases = ['hi there', 'hello', 'hope this email finds you', 'i hope', 'reaching out', 'just wanted to', 'circle back'];
        const hasBannedPhrase = bannedPhrases.some(phrase => email.body.toLowerCase().includes(phrase));
        if (!hasBannedPhrase) score += 20;

        // Check for hyphens
        if (!email.body.includes(' - ') && !email.body.includes(' – ')) score += 10;

        // Check for personalization
        if (email.body.includes(email.to.split('@')[1])) score += 15;

        // Check for specific numbers/data
        const hasNumbers = /\d+%|\$\d+|X increase/.test(email.body);
        if (hasNumbers) score += 15;

        // Check for clear CTA
        const hasCTA = /\?$|calendar|demo|show you|send it|worth/i.test(email.body);
        if (hasCTA) score += 15;

        // Check length (not too long)
        const wordCount = email.body.split(' ').length;
        if (wordCount >= 80 && wordCount <= 200) score += 15;

        // Check for story structure
        const hasStory = email.body.split('\n\n').length >= 3;
        if (hasStory) score += 10;

        return score;
    }

    matchICP(leadData) {
        // Match lead to ICP based on revenue, industry, etc.
        if (leadData.revenue === '$100M+' && leadData.industry === 'Technology') {
            return { name: 'enterprise_saas', ...this.icpProfiles.enterprise_saas };
        }
        if (leadData.revenue === '$50M-100M') {
            return { name: 'growth_tech', ...this.icpProfiles.growth_tech };
        }
        return { name: 'enterprise_saas', ...this.icpProfiles.enterprise_saas };
    }

    matchPersona(title) {
        title = title.toLowerCase();

        if (title.includes('cro') || title.includes('chief revenue')) {
            return { name: 'chief_revenue_officer', ...this.buyerPersonas.chief_revenue_officer };
        }
        if (title.includes('vp') && title.includes('sales')) {
            return { name: 'vp_sales', ...this.buyerPersonas.vp_sales };
        }
        if (title.includes('caio') || title.includes('chief ai')) {
            return { name: 'chief_ai_officer', ...this.buyerPersonas.chief_ai_officer };
        }
        if (title.includes('ceo') || title.includes('founder')) {
            return { name: 'ceo_founder', ...this.buyerPersonas.ceo_founder };
        }
        if (title.includes('director') && (title.includes('rev') || title.includes('sales ops'))) {
            return { name: 'director_rev_ops', ...this.buyerPersonas.director_rev_ops };
        }

        return { name: 'vp_sales', ...this.buyerPersonas.vp_sales };
    }

    detectTriggers(leadData) {
        const detected = {};

        // Simulate trigger detection (in production, would query data sources)
        if (leadData.recentFunding) {
            detected.funding_event = {
                amount: leadData.fundingAmount,
                ...this.triggers.funding_event
            };
        }

        if (leadData.newHire && leadData.daysInRole < 90) {
            detected.leadership_change = {
                days_ago: leadData.daysInRole,
                ...this.triggers.leadership_change
            };
        }

        detected.company = leadData.company;
        detected.quarter = 'Q4';

        return detected;
    }

    // Quality Control: Only send emails scoring 85+
    approveForSending(emailResult) {
        if (emailResult.qualityScore >= this.qualityThreshold) {
            return {
                approved: true,
                message: `Email approved (Score: ${emailResult.qualityScore}/100)`
            };
        } else {
            return {
                approved: false,
                message: `Email rejected (Score: ${emailResult.qualityScore}/100). Needs improvement.`,
                improvements: this.suggestImprovements(emailResult.email)
            };
        }
    }

    suggestImprovements(email) {
        const improvements = [];

        if (email.body.toLowerCase().includes('hi ') || email.body.toLowerCase().includes('hello')) {
            improvements.push('Remove "Hi/Hello" opening');
        }
        if (email.body.includes(' - ')) {
            improvements.push('Remove hyphens');
        }
        if (email.body.split(' ').length < 80) {
            improvements.push('Add more story/context');
        }
        if (!(/\?$/.test(email.body))) {
            improvements.push('End with clear question/CTA');
        }

        return improvements;
    }
}

// Export for use in demos
if (typeof module !== 'undefined' && module.exports) {
    module.exports = OutreachAgent;
}

#!/usr/bin/env python3
"""
Load world-class conversation patterns into vector database
"""

import os
import sys
import json
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.analyzer import SalesConversationAnalyzer
from src.vector_store import VectorStore


# World-class example conversations
WORLD_CLASS_EXAMPLES = [
    {
        "transcript": """
Agent: Hi Sarah, thanks for taking my call. I noticed your company recently raised Series B funding. Congratulations!

Prospect: Thank you! Yes, we're excited about it.

Agent: That's great. As you scale, what's the biggest operational challenge you're facing right now?

Prospect: Honestly, our sales team is struggling to keep up. We're getting leads but can't follow up fast enough.

Agent: I see. How is that affecting your ability to capitalize on the funding and hit your growth targets?

Prospect: We're probably losing 30-40% of qualified leads. It's costing us at least $200K per quarter in missed revenue.

Agent: If this continues for the next two quarters while you're trying to prove the value of that Series B investment, what's at stake?

Prospect: Our growth trajectory. We need to show investors we can execute. If we keep missing revenue targets, it puts everything at risk.

Agent: That's significant. If you could solve this and capture even half of those missed leads, what would that mean for your business?

Prospect: That's an extra $400K in revenue. We'd hit our targets and show strong momentum to investors.

Agent: Exactly. That's what we help companies do - capture those missed opportunities automatically. Given the urgency and what's at stake, when would be the best time to implement a solution like this?

Prospect: We need to move quickly. Can we do a trial next week?

Agent: Absolutely. Let's get you set up for Tuesday. I'll have our implementation team reach out today.
        """,
        "metadata": {
            "conversation_id": "wc_001",
            "outcome": "booked_demo",
            "deal_value": 50000,
            "industry": "SaaS",
            "effectiveness_note": "Perfect SPIN execution with quantified pain amplification"
        }
    },
    {
        "transcript": """
Agent: Mike, most B2B companies your size think the main challenge is lead generation. But we're seeing something different across our 500+ clients.

Prospect: Oh? What are you seeing?

Agent: The real problem isn't getting leads - it's that 70% of qualified leads never get contacted within 5 minutes. And here's the surprising part: response time is the #1 predictor of whether a lead converts.

Prospect: That's interesting. We do have a follow-up problem.

Agent: Right. And for a company at your stage - $10M ARR, looking to hit $25M in 18 months - every missed lead is roughly $15K in lost LTV. Given your current lead volume, you're likely leaving $2-3M on the table annually.

Prospect: That's... significant. I hadn't thought about it that way.

Agent: Most founders don't until they see the numbers. Here's what I recommend: let's run a 30-day pilot where we handle your lead response. You'll see exactly how much revenue you're missing. If it's substantial, we implement fully. If not, you've lost nothing. Sound fair?

Prospect: Yeah, that makes sense. When can we start?

Agent: I'll have our team set everything up by Friday. You'll have full visibility into every lead and response time.
        """,
        "metadata": {
            "conversation_id": "wc_002",
            "outcome": "closed",
            "deal_value": 75000,
            "industry": "SaaS",
            "effectiveness_note": "Excellent Challenger Sale - taught new perspective, tailored to their stage, took control"
        }
    },
    {
        "transcript": """
Agent: Jennifer, walk me through what your sales process looks like today.

Prospect: We have about 10 reps. They manually enter leads, make calls, send follow-ups. It's all very manual.

Agent: Okay. And what would the ideal scenario look like? If you could wave a magic wand?

Prospect: Leads would automatically be distributed, reps would have scripts and talking points ready, follow-ups would be automated, and we'd have real-time visibility into pipeline.

Agent: Perfect. So the gap is going from manual, time-consuming processes to automated, efficient workflows. What's that gap currently costing you?

Prospect: Our reps spend 3-4 hours a day on admin work instead of selling. That's probably costing us 40-50% of their productivity.

Agent: Right. So you're paying for 10 reps but getting the output of 5-6. At an average of $100K per rep, that's $400-500K in wasted salary annually, plus all the missed revenue.

Prospect: Wow. I've never calculated it like that.

Agent: Most people haven't. The gap between where you are and where you want to be is costing you roughly $1M per year in direct and opportunity costs. How quickly do you want to close that gap?

Prospect: As soon as possible.

Agent: Great. Let's schedule implementation for next Monday. I'll need about 2 hours with your sales manager to map out the workflows.
        """,
        "metadata": {
            "conversation_id": "wc_003",
            "outcome": "closed",
            "deal_value": 60000,
            "industry": "B2B Services",
            "effectiveness_note": "Textbook Gap Selling - quantified current state, future state, and the gap"
        }
    },
    {
        "transcript": """
Agent: David, before we dive in, let me set expectations. At the end of this call, you'll either see clear value and we'll move forward, or you'll know this isn't for you. Either way, you'll have clarity. Sound fair?

Prospect: Sure, that works.

Agent: Great. Tell me, what made you take this call today?

Prospect: We're struggling with customer retention. Churn is killing us.

Agent: Okay. Is fixing churn a priority issue or a back-burner issue?

Prospect: It's definitely a priority. We're losing revenue faster than we're gaining it.

Agent: I see. And if you don't fix this in the next 90 days, what happens?

Prospect: We'll probably miss our quarterly targets and have to lay people off.

Agent: That's serious. Do you have budget allocated to solve this?

Prospect: We do. We set aside $50K for a retention solution.

Agent: Perfect. And who else is involved in this decision?

Prospect: Just me. I'm the CEO.

Agent: Okay, so you have a priority problem, budget available, and decision authority. If I can show you how to cut churn by 40% in 90 days, is there any reason we wouldn't move forward today?

Prospect: No, if you can deliver that, let's do it.

Agent: Excellent. Let's get the paperwork started. I'll send the contract over in the next hour.
        """,
        "metadata": {
            "conversation_id": "wc_004",
            "outcome": "closed",
            "deal_value": 50000,
            "industry": "SaaS",
            "effectiveness_note": "Perfect Sandler execution - upfront contract, pain-budget-decision qualification"
        }
    },
    {
        "transcript": """
Agent: Lisa, you mentioned price is a concern. It seems like you're worried about spending $30K on something that might not deliver results. Is that accurate?

Prospect: Yeah, exactly. It's a lot of money.

Agent: I understand. It sounds like you're also concerned about what your CFO will say. Am I reading that right?

Prospect: You are. He's very conservative with spending.

Agent: Okay. Help me understand - how much is your current approach costing you per month in lost opportunities?

Prospect: Probably around $50-60K per month.

Agent: So you're currently losing $50-60K monthly, which is $600-720K annually. And you're hesitant to invest $30K to stop that bleeding?

Prospect: When you put it that way...

Agent: What am I missing? What would need to be true for this to be a no-brainer?

Prospect: I guess if I could show the CFO a clear ROI within 3 months.

Agent: That's fair. What if we structured it so you only pay half upfront, and the other half after you see $100K in recovered revenue? That way, the solution essentially pays for itself.

Prospect: That would work. Let's do that.

Agent: Perfect. I'll draft the terms and send them over by end of day.
        """,
        "metadata": {
            "conversation_id": "wc_005",
            "outcome": "closed",
            "deal_value": 30000,
            "industry": "E-commerce",
            "effectiveness_note": "Excellent Chris Voss techniques - labeling, calibrated questions, finding the black swan"
        }
    }
]


def main():
    print("🌟 Loading World-Class Conversation Patterns...")

    # Initialize analyzer and vector store
    analyzer = SalesConversationAnalyzer(
        vector_db_path="./data/vector_db"
    )

    print(f"\n📚 Processing {len(WORLD_CLASS_EXAMPLES)} world-class examples...")

    successful = 0
    failed = 0

    for i, example in enumerate(WORLD_CLASS_EXAMPLES, 1):
        try:
            print(f"\n📖 Example {i}/{len(WORLD_CLASS_EXAMPLES)}: {example['metadata']['conversation_id']}")

            # Analyze the conversation
            analysis = analyzer.analyze(
                transcript=example["transcript"],
                metadata=example["metadata"],
                use_ai=False  # Skip AI analysis for speed
            )

            # Verify it was stored (high effectiveness patterns are auto-stored)
            if analysis.training_value in ["high", "medium"]:
                print(f"   ✅ Stored in vector database")
                print(f"   📊 Effectiveness: {analysis.effectiveness_score:.2f}")
                print(f"   🎯 Patterns: {len(analysis.key_patterns)}")
                successful += 1
            else:
                print(f"   ⚠️  Not stored (effectiveness: {analysis.effectiveness_score:.2f})")
                failed += 1

        except Exception as e:
            print(f"   ❌ Error: {e}")
            failed += 1

    # Get final statistics
    stats = analyzer.vector_store.get_statistics()

    print("\n" + "="*60)
    print("📊 LOADING COMPLETE")
    print("="*60)
    print(f"✅ Successfully loaded: {successful}")
    print(f"❌ Failed: {failed}")
    print(f"📚 Total conversations in database: {stats.get('total_conversations', 0)}")

    if stats.get('database_type') == 'json':
        positive = stats.get('positive_outcomes', 0)
        high_value = stats.get('high_training_value', 0)
        avg_effectiveness = stats.get('avg_effectiveness_score', 0)

        print(f"🎯 Positive outcomes: {positive}")
        print(f"⭐ High training value: {high_value}")
        print(f"📈 Average effectiveness: {avg_effectiveness:.2f}")

    print("\n✨ World-class patterns are now available for:")
    print("   - Training AI agents")
    print("   - Real-time conversation assistance")
    print("   - Gap analysis and coaching")
    print("   - Pattern matching and retrieval")

    print("\n🚀 Ready to build world-class sales conversations!")


if __name__ == "__main__":
    main()
